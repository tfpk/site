~~~
md_name = "profiling"
name = "Adventures in Profiling"
desc = "How I learned to stop worrying and love losing three days of work"
image = "images/cowboy_bomb.jpg"
~~~

Recently, I was given a task at my workplace, [Kinesis](kinesis.org.au). Take a function that runs in 120 seconds, and speed it up.
I eagerly went about doing some refactoring!

_This example has been heavily altered because I like my job_: We have data on weather events, some of which is reported by humans, and some by 
measuring stations. Measuring stations also have data on atmospheric conditions at the start and end of the rainstorm, which are in a
seperate dataset. The function had to merge the atmospheric information onto the column that shows the start time (as a string) of the weather event, and the end time (as a string). Finally,
go through the new dataset, and if the event was recorded at a weather station, replace the name of the person who reported it at the 
weather station, with the weather station's name.

There was one other catch: we didn't control the programs that used this data. We had access to their source code,
but nobody really knew how it worked. A lot of exploring and trial-by-error was required to actually figure out what these functions did and didn't need.

I set about reading the source code we had and playing around with the black-box programs a bit, and it turned out that we used this function twice, and both times we only cared
about some atmospheric data, and some types of weather events. 
It was suggested to me I should look at cutting down the number of rows. My experience with algorithmic complexity suggested this would make
sense too: A merge function is likely to be on the order of `O(n*log(n))` - that's probably the most complex problem in the code 
(and the merge happens twice!). Easy wins.

I had a nice pytest suite, so my plan was simple: try to observe what data I could cut, make some filters on the data, and check each time 
I changed something that I didn't change the results of the test suite, and that I made it faster.

I spent a few hours on this approach, cutting down from an initial `1000000` rows we were merging on to around `860000`. This sped up the program a little - awesome!
The approach wasn't long lived though: there was a lot of data, and I couldn't cut down much more of it.

My next observation was this: the places we used this data cared about *different* things for the start and end time data!
I could cut the data more if I treated it differently for the start-time and end-time. So I did some more filtering, and lo we went to about `800000` rows being merged!
Again, this hit a road-block as I couldn't cut any more data. The program *was* running faster: I had cut 20 or so seconds off it's time.

A third observation now: the programs that used this data actually cared about different subsets of the rows.
I figured the easy solution was to give them seperate data, so I wrote wrapper functions for each of the programs to call.
Great! I did some more filtering, and one of the programs went from getting `800000` rows, to getting `100000`.
The other program was more obstinate, but I still cut down to around `680000` rows.

At this point, there was no more cutting I could do: all the rows were needed for the programs to produce the correct output. But I wanted to keep speeding up the programs,
and the imbalance in the programs bothered me.

I then started googling for "how to speed up pandas merges". Google, being the panacea for all human ills, returned [this article](https://stackoverflow.com/questions/50970859/merging-dataframes-on-an-index-is-more-efficient-in-pandas).
I tried to use `set_index`, but could not get it to work properly. To this day I'm not entirely sure why, but I think it was because there were multiple identical rows in the dataset (that needed to be there), and pandas seemed not to preserve them.
The solution I arrived at was this: I may not be able to set index, but pandas merges are faster when merging on integers.

I cooked up a quick script that mapped the strings that had the start-time and end-time into integers (I couldn't map them to datetime types - I tried, and it wouldn't work). The performance gain was stark: Programs that ran in 20 and 80 seconds respectively now ran in 4 and 20. Sweet!
I had a lingering feeling that this script was going too far into something pandas should be able to do itself. I tried to replace the script with casting everything to categoricals, but that didn't retain the speed benefits. It looked like I had to stick with this slightly ugly script.
The performance gains were probably worth it.

At this point I approached my colleague to greet him with the good news! He looked at my code, and we spent a few hours going back and forth over whether I could in fact cast the datetime strings to datetimes, or cast them to categoricals. It turned out he could not either.

His next suggestion was the key to me wanting to write this entire article: "Okay Tom, lets go back through your changes in stages, and profile them to see which optimisation helps the most. Hopefully we don't have to put all of them into prod, because there's a lot of specific code".

So, I stashed my changes, and applied them again in stages. The performance drops were exactly as I had said above, and the best optimisation was doing the mapping to integers: it alone cut the time to run from 120 seconds down to 30 or so. I'm not an expert at c-profile, so I did things
the 'easy way': print out after each line with the number of seconds the previous line took to ran. It was at this point I realised something: the last step of the program, which I had not considered at all (it was `O(N)`, so surely it wasn't expensive) took a long time to run.
I investigated further: it took about 90% of the time the program took to run. I hadn't noticed that because it went down proportonally to the other changes I made, but it was the vast majority of the problem.

Realising this, I experimented with other ways of implementing it. It was implemented as a lambda that was applied to every row. After some googling, I found the pandas `where` function, which could be used to do the exact same thing as the lambda.
The performance gains were staggering: code that took 160 seconds to run now ran in 1 second. I realised that the effort I had spent -- for 3 days -- could have been achieved by a 10 line diff.

Looking back on it, I learned a lot in the time I spent, but I'm the sort of person who has a hard time forgiving themselves for making mistakes. If you are too, here's the most important takeaways:

 - Profile your code before you refactor it. Even if you think you know where it's most complex, you might be wrong. Ten minutes of profiling the code would have saved me two and a half days' work.
 - Listen to your gut when code looks messy, even when it's a performance optimisation. Of course I know that sometimes performant code needs to be more hacky, but had I been more sensitive to it earlier, I might have gone looking
   for ways to improve performance without writing my own hacky code.
 - In Python, wherever you can farm your work out to C or Fortran, do it. Using a lambda, or using a function to do mappings is all well and good, but pandas has functions that are way faster. Use them where you can.

