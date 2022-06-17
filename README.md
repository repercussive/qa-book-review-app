# Book Review App - "Pageturner"
## Liam Robertson

This repo includes my deliverable files for the QA DevOps Core Fundamental Project.

## Contents
1. [Project requirements](#project-requirements)
2. [Design](#design)
3. [Project tracking](#project-tracking)
4. [Risk assessment](#risk-assessment)
5. [Development process](#development-process)
6. [Testing](#testing)
7. [Automation](#automation)
8. [The app](#the-app)
9. [Known issues](#known-issues)
10. [Future developments](#future-developments)
11. [Acknokwledgements](#acknowledgements)

## Project requirements

The overall objective for this project was to develop a web application featuring CRUD (create, read, update & delete) functionality. The project must satisfy the following requirements:

* CRUD app created in Python
* functioning front-end website and integrated APIs using the Flask micro-framework
* a relational database to store data persistently - the database needs to have at least 2 related tables
* test suites with high test coverage
* code integrated into a Version Control System
* automated testing/deployment pipeline using cloud-based virtual machines
* a kanban board to track project tasks/progress
* clear documentation outlining project design and architecture

## Design
I have chosen to create a website which allows users to find and write book reviews. This satisfies the four aspects of CRUD as follows:

* CREATE: users can add books and reviews to the database
* READ: users can view the books in the database and their reviews
* UPDATE: users can edit the details of books and their reviews
* DELETE: users can delete books and reviews

### Database model
For the minimum viable product (MVP) I initially designed the application to use only two database tables - one for **books**, and one for **reviews**. The model for this is shown in the ERD below.

| ![image](https://user-images.githubusercontent.com/7796522/174313158-b615dce6-ab99-4a9d-b5e8-b599571ec056.png) | 
|:--:| 
| *This is a one-to-many relationship, where each book can have many reviews.* |

After all the basic project requirements were met, the app’s functionality was extended through the addition of a **genres** feature, allowing each book to have multiple genres associated with it. The updated database model is shown and described below.

| ![image](https://user-images.githubusercontent.com/7796522/174314629-9b33ffd9-6254-47b9-a066-71989f95599a.png) | 
|:--:| 
| *The one-to-many relationship between books and reviews remains. The relationship between books and genres is many-to-many, as one book can have multiple genres associated with it, and one genre can have many books associated with it. The relationship is facilitated by the association table **book_genre**.* |

The above model was successfully implemented in the app, as seen [here](https://github.com/repercussive/qa-book-review-app/blob/dev/application/models.py).

### UI design
I created mockups for the front-end views using Figma, which can be found [here](https://www.figma.com/file/YOPICwc7roaCjWeBHTCTjG/Untitled?node-id=41%3A2). Following these designs streamlined the development process, as I always had in mind the final product I was working towards.

### Project tracking
To track the progress of the project I used Jira. Before starting development, I determined all of the tasks that would need to be completed to create the project, and added these tasks to the Jira kanban board. Tasks would be moved to the “In progress” column while being developed, and then to “Done” when completed. After all of the MVP tasks were completed, I added new tasks related to the implementation of the genres feature under a separate Epic. Shown below is the state of the Jira board during the middle of development.

![image](https://user-images.githubusercontent.com/7796522/174315551-a9632db7-cd5a-4edc-b279-9e2812fbad12.png)

## Risk assessment
I performed a simple risk assessment outlining some hazards, their impacts, as well as responses and control measures. [This risk assessment matrix](https://www.researchgate.net/profile/Gulsum-Kaya/publication/323570642/figure/fig7/AS:625770716217345@1526206773610/A-standard-risk-matrix.png) illustrates the system used. For each hazard, the likelihood and impact are rated on a scale from 1 to 5, and the priority level is calculated as the product of these two ratings. 

![image](https://user-images.githubusercontent.com/7796522/174316650-f90e581f-5a89-4a54-8d07-0d4b22f079f5.png)

Many of these control measures listed were implemented in this project, for example:

* Control measure for the hazard “Jenkins VM goes down”: pipeline scripts are not stored on the Jenkins machine, but rather in this repo - see [Jenkinsfile](https://github.com/repercussive/qa-book-review-app/blob/dev/Jenkinsfile) and [deploy.sh](https://github.com/repercussive/qa-book-review-app/blob/dev/deploy.sh)
* Control measure for the hazard “Sensitive credentials leaked to GitHub” : no credentials are stored in this repository and instead are stored in environment variables on the relevant virtual machines

Some control measures were not implemented, for example encryption was not used. This is because, in the project’s current state, no personal user data is stored in the database. However, if the application was updated to include a password login system for example, then this data would need to be encrypted securely.

## Development process
Version control was used throughout development of the project. The VCS used was **git**. Git allows changes to be batched into commits and further organised into branches. Each commit acts as a snapshot of the project at a given point in time, so the commit history allows me to access previous versions. The **dev** branch acts as the primary branch used for development. However, commits were rarely made directly to the dev branch - instead, when working on a new feature, I would create a separate feature branch. When the feature was completed the changes were merged into the dev branch. This keeps the dev branch stable and prevents half-completed features from being deployed. Upon reaching a major version the dev branch is merged into **main**.

The project repo is hosted on GitHub. I frequently pushed my changes to the remote repository. It not only acts as a backup for the project files, but it also provides additional features such as webhooks. GitHub will send an HTTP POST request to the build server when changes are pushed, allowing for automated testing, building and deployment of the app.

The app was developed in Python, using the web micro-framework Flask. CRUD operations are implemented as functions associated with Flask routes. The front end is implemented with Jinja2 templates, which are mostly HTML. Flask evaluates the Jinja templates and send HTML files populated with dynamic data to the user. The front end was styled using CSS. The development environment was a Python virtual environment (venv) hosted on my local machine. Venv allows each project to have its own dependencies, as packages are installed in an isolated environment instead of being installed globally. This prevents conflicts (version differences) with other installs on the host machine. With python3 installed, this environment is easy to replicate:

```bash
python3 -m venv venv
# (linux)
source venv/bin/activate
# (windows)
source venv/Scripts/activate
pip3 install -r requirements.txt
```

Automatic testing, building and deployment were handled by Jenkins, which was used as the build server.

## Testing
Testing was used continuously during the development process to ensure that the app is functioning as intended. I used unit testing - this tests individual units of functionality, namely the create, read, update and delete functions within my application. Tests were written alongside features as they were added. This ensures that I am made aware if features that previously worked begin to break. The unit tests generally send a request to the app, and check that the correct response is returned, or that expected changes to the database were made correctly.

Pytest was used as the testing library for this project. When pytest test suites are run, it gives you a summary of which tests passed and failed, and it can provide detailed coverage reports. The output of a successful test run is shown below.

![image](https://user-images.githubusercontent.com/7796522/174330073-a6442c77-121f-4253-a00f-4629b1ffddd4.png)

According to pytest, 99% overall coverage was achieved. The missing lines are not related to the primary CRUD functions of the application.

Integration testing would have also been desirable for this project, however it was not performed due to time constraints. Other types of testing, such as performance testing, were outside the scope of this project as this is not a real-world production app.

## Automation

This project benefits from an automated test/build/deploy pipeline using Jenkins. On the Jenkins VM, a Pipeline project was set up. When changes are pushed to the dev branch (which, as mentioned, is used for stable versions with completed features), this will trigger a GitHub webhook, which is sent to Jenkins. This will cause the stages in [the Jenkinsfile](https://github.com/repercussive/qa-book-review-app/blob/dev/Jenkinsfile) to run.

Firstly, Jenkins will automatically run the unit tests. If any of the tests fail, the build will be aborted, which prevents faulty versions of the application from being deployed.

Next, Jenkins will copy the project files needed to run the application into the deployment VM. Then it runs the [deploy script] on the deployment VM which installs the project’s dependencies and starts the app using gunicorn, a WSGI server that can run the app on multiple processes (workers) simultaneously.

The final step involves integration with the Cobertura plugin. This takes the XML coverage report generated during the testing stage and displays it within the Jenkins interface, as show below.

![image](https://user-images.githubusercontent.com/7796522/174319802-38e259d4-d34f-4532-943c-9d538c2652c4.png)

***An example of the console output from a successful build can be found [here](https://gist.github.com/repercussive/16ce672843fcbc0b648a3281332a85c7).***

Below is a diagram summarising the CI/CD process used in this project. Note that the SQL instance and virtual machines for this project run on Google Cloud Platform. 

![image](https://user-images.githubusercontent.com/7796522/174319940-95ba5554-768a-448d-86aa-18c252edfc6d.png)

## The app

Here is an overview of the resulting application.

| ![image](https://user-images.githubusercontent.com/7796522/174321430-5027260d-ef6e-43a0-aa5f-a0d4e2d6f0e2.png) | 
|:--:| 
| `[/]` *The app’s home page includes some links to other parts of the app, as well as summaries/links for the most recent reviews added to the database (up to 6). The navbar appears on all pages and allows the user to navigate between the home page, the `books` page, and the `add-review` page.* |

| ![image](https://user-images.githubusercontent.com/7796522/174320738-7308b12f-8dc0-46f4-b94c-49a0ab9431c8.png) | 
|:--:| 
| `[/add-review]` *The `add-review` page contains a form which, when submitted, will add a book review to the database. If the book to be reviewed is not yet in the database, this page contains a link to the `add-book` page, which the user can follow.* |

| ![image](https://user-images.githubusercontent.com/7796522/174320905-485dc878-abc7-4254-9bac-ab527c10fd78.png) | 
|:--:| 
| `[/add-book]` *This page contains a form which, when submitted, will add a book to the database. If the user was directed here from the `add-review` page (in which case the URL query param `toreview` will be true), then after submission the user will be automatically redirected back to the `add-review` page, with the recently added book pre-selected. Otherwise the user will be redirected to the books page.* |

| ![image](https://user-images.githubusercontent.com/7796522/174320976-23ffb61f-b4d2-48ff-af6a-9957aeee6218.png) | 
|:--:| 
| `[/books]` *The `books` page shows a list of all books in the database by default, however it is also possible to filter by a specific genre or search for keywords in book titles. Each book listed contains links to add a review, edit the book, delete the book, or “See all reviews”.* |

| ![image](https://user-images.githubusercontent.com/7796522/174321043-54c2aa97-f9ab-4a28-a0da-03328cf02fa5.png) | 
|:--:| 
| `[/reviews/<book id>]` *When the “See reviews” link is followed, a list is displayed containing all reviews associated with that book, including their ratings, headlines, and authors.* |

| ![image](https://user-images.githubusercontent.com/7796522/174322452-acda22fe-875c-4cda-910e-fcd0a296312c.png) | 
|:--:| 
| `[/review/<review id>]` *After following the “Read review” link from the previous page, a more detailed page is displayed, containing the body of the review. There are also links to edit and delete the review.* |

## Known issues
* There is nothing to prevent two identical books (with the same title and author) from being added
* The app has limited error handling, e.g. if the user navigates to /review/999 (and there is no review with id 999) the app will simply display the traceback instead of showing a “Not found” page, or redirecting the user to an existing page

## Future developments
The app in its current state is quite rudimentary. The main way to develop this project further would be to add user accounts. This would present quite a few challenges related to security and user authentication. However, it would open up the door to more features such as:
* Users could add books to their own personal reading lists
* Reviews would be tied to a user, and could only be edited/deleted by that user (instead of being editable by anyone)

## Acknowledgements
Thanks to Earl, Adam and Leon for their guidance on this project.
