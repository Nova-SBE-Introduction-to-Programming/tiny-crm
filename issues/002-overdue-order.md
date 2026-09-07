# Overdue follow-ups: wrong count, and the wrong leads get flagged

**What I did**

Looked at the "Overdue follow-ups" number on the Pipeline page and then went through the leads one by one to check which ones are marked overdue (the red "overdue" tag next to the follow-up date). Today is 31 August 2026.

**What I expected**

Every open lead with a follow-up date before today to be flagged, and the number to match. I count 8 of those in the list.

**What actually happened**

The number says 4. Rui Martins (follow-up 2026-08-12) is flagged, fine. But Ana Ferreira has follow-up 2026-8-5, which is even older, and she has no tag at all. Same for Pedro Santos (2026-7-30), Nuno Rocha (2026-8-27) and Hugo Barbosa (2026-8-18): all clearly in the past, none flagged. It looks like the ones that slip through are all dates written like `2026-8-5` instead of `2026-08-05`, and we do have a mix of both in the file because some were typed by hand. If I sort the flagged ones in my head they also come out in a strange order, as if the dates were sorted as words and not as dates.
