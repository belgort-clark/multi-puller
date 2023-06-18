# Multi-Puller
# Forked from https://github.com/philbowman/multi-puller
# Modified to work for CS50P

import subprocess  # used to execute external programs
import os
import csv
from pathlib import Path
from datetime import datetime
import shutil  # used for copying/moving files and more
import git  # used to interact with git/github (gitpython)

STUDENTWORK_DIR = "studentwork/"
COMPARE50_DIR = "compare50"
COURSE_ID = "XXXX"

if not os.path.exists(STUDENTWORK_DIR):
    subprocess.run("mkdir " + STUDENTWORK_DIR, shell=True)


def run_compare50(slug, foldername, archive_path):
    print("Running compare50..")
    assignment_path = STUDENTWORK_DIR + foldername
    archive_folder = str(Path().resolve().parent) + "/studentwork/" + archive_path
    print(f"Archive folder: {archive_folder}")
    output_dir = f"{assignment_path}/{COMPARE50_DIR}"
    if os.path.exists(assignment_path + "/distro"):
        distro = " -d " + assignment_path + "/distro/*.py"
    else:
        distro = ""
    if os.path.exists(output_dir):
        print("archiving old compare50 output...")
        archive_dir = output_dir + "_archived_" + datetime.now().strftime("%Y%m%d")
        if os.path.exists(archive_dir):
            shutil.rmtree(archive_dir)
        os.rename(output_dir, archive_dir)

    if os.path.exists(archive_folder):
        print(f"slug: {slug}\nfoldername: {foldername}\narchive_path: {archive_path}")
        print(
            f"compare50 {assignment_path}/*/*.py -a {archive_folder}/*/*.py -o {output_dir}{distro}"
        )
        subprocess.run(
            f"compare50 {assignment_path}/*/*.py -a {archive_folder}/*/*.py -o {output_dir}{distro}",
            shell=True,
        )
    else:
        print("no archive found")
        print(f"compare50 {assignment_path}/*/*.py -o {output_dir}{distro}")

        subprocess.run(
            f"compare50 {assignment_path}/*/*.py -o {output_dir}{distro}", shell=True
        )


def list_submissions(slugs):
    # print(slugs)
    if os.path.exists(STUDENTWORK_DIR + "list.html"):
        archive_file = (
            STUDENTWORK_DIR
            + "list_archived_"
            + datetime.now().strftime("%Y%m%d")
            + ".html"
        )
        if os.path.exists(archive_file):
            os.remove(archive_file)
        os.rename(STUDENTWORK_DIR + "list.html", archive_file)
    with open(STUDENTWORK_DIR + "list.html", "a") as file:
        for slug in slugs:
            assignment_path = STUDENTWORK_DIR + slug["folder"]
            print(assignment_path)
            if os.path.exists(assignment_path):
                if os.path.exists(assignment_path + "/" + COMPARE50_DIR):
                    file.write(f"<h1>{slug['folder']}</h1>")
                    file.write("<p>" + slug["slug"] + "</p>")
                    file.write(
                        '<p><a href="file://'
                        + os.path.abspath(assignment_path + "/" + COMPARE50_DIR)
                        + '/index.html" target="_blank">'
                        + "compare50"
                        + "</a> | "
                    )
                    file.write(
                        f"<a href=\"https://submit.cs50.io/courses/{COURSE_ID}/{slug['slug']}\" target=\"_blank\">me50</a> | \n"
                    )
                    file.write(
                        f'<a href="file://{os.path.abspath(assignment_path)}" target="_blank">folder</a></p>'
                    )
                else:
                    file.write("<h1>" + slug["folder"] + "</h1>" + "\n")
                with open("students.csv") as students:
                    file.write("<ol>")
                    for person in csv.DictReader(students):
                        if os.path.exists(assignment_path + "/" + person["folder"]):
                            student_folder = assignment_path + "/" + person["folder"]
                            file.write(
                                f"<li><a href=\"https://github.com/me50/{person['username']}/tree/{slug['slug']}\" target=\"_blank\">"
                            )
                            file.write(person["folder"] + "</a> | ")
                            file.write(
                                f'<a href="file://{os.path.abspath(student_folder)} "target="_blank">folder</a>'
                            )

                            repo = git.Repo(student_folder)
                            branch = repo.head.reference
                            print(student_folder)
                            submitted = False
                            for commit in repo.iter_commits():
                                if "submit50" in commit.message:
                                    submitted = True
                                    submit_commit = commit
                                    break
                            if "check50" in branch.commit.message:
                                file.write(" [check50]\n")
                                if submitted:
                                    file.write(
                                        f"<a href=\"https://github.com/me50/{person['username']}/tree/{commit.tree}\" target=\"_blank\">submit50</a>"
                                    )

                            file.write("</li>\n")

                        else:
                            file.write("<li><s>" + person["folder"] + "</s></li>\n")
                    file.write("</ol>")
                file.write("\n")
    print("file://" + os.path.abspath(STUDENTWORK_DIR + "list.html"))


def get_projects(slug, foldername):
    print(f"fetching student work for {slug}")
    assignment_path = STUDENTWORK_DIR + foldername

    # make the assignment folder.
    if not os.path.exists(assignment_path):
        subprocess.run("mkdir " + assignment_path, shell=True)

    # iterate over students in students.csv
    try:
        with open("students.csv") as students:
            for person in csv.DictReader(students):
                github_url = "https://github.com/me50/" + person["username"]
                student_path = assignment_path + "/" + person["folder"]

                # pull/update repos that have already been cloned
                if os.path.exists(student_path):
                    print(f"{student_path} exists; pulling...")
                    subprocess.run("git pull --rebase", shell=True, cwd=student_path)

                # clone repos that haven't yet been cloned
                else:
                    print(f"{student_path} doesn't exist. cloning {github_url}")
                    subprocess.run(
                        f"git clone -b {slug} {github_url} {person['folder']}",
                        shell=True,
                        cwd=assignment_path,
                    )

    except FileNotFoundError:
        print("students.csv does not exist")


def get_assignments():
    foldernames = []
    try:
        # iterate over list of assignments in slugs.csv
        with open("slugs.csv") as slugs:
            for slug in csv.DictReader(slugs):
                # use user-defined local folder name
                slug_arr = slug["slug"].split("/")

                # create folder names for "more" and "less" assignments
                if slug_arr[-1] == "less" or slug_arr[-1] == "more":
                    foldername = f"{slug_arr[-2]}_{slug_arr[-1]}"
                    archive_path = f"{slug_arr[-2]}"
                else:
                    foldername = slug_arr[-1]
                    archive_path = slug_arr[-1]

                # override the foldername
                if slug["folder"]:
                    foldername = slug["folder"]

                get_projects(slug["slug"], foldername)
                run_compare50(slug["slug"], foldername, archive_path)
                foldernames.append({"folder": foldername, "slug": slug["slug"]})

        list_submissions(foldernames)

    except FileNotFoundError:
        print("slugs.csv does not exist")


get_assignments()
