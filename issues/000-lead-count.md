# The numbers at the top of the pipeline are wrong

**What I did**

Opened the app, looked at the five numbers across the top of the Pipeline page (new, contacted, proposal, won, lost). Then I scrolled down and counted the leads listed under each stage by hand.

**What I expected**

The number above each stage to be the number of leads listed under that stage. Boring, I know, but that is the whole point of the numbers.

**What actually happened**

Every single number is one higher than what is listed. "new" says 9, I count 8. "lost" says 5, I count 4. Same for the others. I added a lead and the "new" number went from 9 to 10, so it does follow the data, it is just always one too many. I also reset the data with `python seed.py` and it is still off by one, so it is not something I broke.
