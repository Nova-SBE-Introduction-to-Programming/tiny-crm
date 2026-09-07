# Onboarding sheet — Tiny CRM

Group: ____________   Members: ____________________________

Answer in this file, inside your project folder. Use the AI as much as you like — then verify every answer in the code or by clicking. Write *where* you verified (file + line, or what you clicked).

## Ask the code

1. In one sentence, what does Tiny CRM do for its user?
2. Which file runs first when you start the app? How do you know?
3. Where is the data stored? Name the file and the three tables.
4. Click **Move to next stage** on a lead. Which function runs? Which function does *that* call to save it?
5. `get_lead` is used in more than one place. Where? Why is it a function instead of copy-pasting the code?
6. Create a lead with an empty name, and one with a follow-up date in the past. What happens? Find the line that should have stopped you.

## Verify the AI

7. Ask the AI: *"What happens to a lead's notes when the lead is deleted?"* Then do it. Was the AI right? Paste its answer and what actually happened.
8. Ask the AI to explain `overdue_followups`. Find one thing it glossed over or got wrong.
9. **Bug #1** — `issues/001.md`: *"Searching for 'acme' finds nothing, but 'Acme' works."* Reproduce it. Name the line. Fix it. Save the file and check the app shows the right result now.
10. Three questions you'd ask the developer who left.

## Done when
- [ ] All laptops run the app
- [ ] This file is answered (it lives in your folder — keep the folder, next week it becomes a repo)
- [ ] Bug #1 fixed and shown to the TA (before / after)
