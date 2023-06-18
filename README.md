## Multi-Puller ##

## Notes from Bruce Elgort

https://gitpython.readthedocs.io/en/stable/

pip install gitpython

This script is for teachers of CS50P.  It will let you pull all the student work for a number of assignments, into folders that you name or that are auto-generated from the slug.  The script then runs compare50 against other student submissions and against archived submissions (I use Douglas Kiang's source50 repo) and creates a list of submissions as `list.html`.

Run the script with `python3 puller.py`.

- This script does not handle authentication with GitHub. You must set up an SSH key according to the instructions [here](https://cs50.readthedocs.io/github/).
- You must create `slugs.csv` and `students.csv`. Templates are proivded.
- Students listed in `students.csv` should have already joined your me50 class. Otherwise, you won't have access to their private me50 repo.
- By default, student repos will be cloned into `[location_of_puller.py]/studentwork/[assignment folder]/[student folder]` where "student folder" is defined in students.csv and "assignment folder" is defined in slugs.csv OR is auto-generated from the last term in the slug (or two terms if the last term is "more" or "less").
  - `cs50/problems/2021/fall/mario/more` becomes `mario_more` 
  - `cs50/problems/2021/fall/cash` becomes `cash`

- If a repo has already been cloned into the folder specified in students.csv, the script will pull the latest changes. 

- If a student has not turned in an assignment, the script simply does not create a folder for that assignment for that user

- You can compare work with [cs50's compare tool](https://cs50.readthedocs.io/projects/compare50/en/latest/) with from the assignment folder wtih, for example, `compare50 studentwork/mario_more/*/*.c -o studentwork/mario_more/compare50` or `compare50 puller/studentwork/cash/*/*.c -a source50/cash/*/*.c -o puller/studentwork/cash/compare50`

This project is based on [puller by Mark Sobkowicz](https://github.com/sobko/puller)
