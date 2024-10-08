# Marathon running app

## R1 

The Marathon Running API is designed to bring runners together. It has functionality for runners to log their workouts and keep track of workout sessions. In the workout log feature, users are allowed to choose from one of the available run types. Date and distance in kilometers are also required to ensure the log keeps all the crucial information for users to track their best sessions. However, the main functionality of my API is to allow users to be part of running groups. 

Running alone can sometimes feel a bit lonely, but when you run in a group, it encourages you to push yourself a little harder, and then the run becomes more enjoyable. This app strives to motivate it's members through accountability to achieve a healthier life style. The goal is to turn exercising into a fun and engaging experience rather than a chore.

Each group will have an admin who will enroll their group in marathons created by different group admins. It’s very practical for users: they can check the available groups and choose which group they want to join, and they can even be part of more than one group. When checking the groups, users will be able to see who the admin of that group is, the group’s members, and what marathons that group is currently enrolled in.

Admins are responsible for creating marathon events and managing any changes, such as location or date.This app takes out all of the hassle log into marathon events individually. Users simply need to select a group and lace up their best pair of shoes to start running.

I believe this app combines two important things: staying healthy and making friends. It also very flexible, allowing the members to choose what group resinates more with them and having the choice to leave the group at any time. 


## R2 

I have tracked tasks and changes using GitHub and Trello. To manage the development of different features—especially since this was my first time creating an API. I created a new branch for each feature. This approach allowed me to keep a clear record of all changes in case I needed to revert to previous code. In total, I have created nine different branches for this project. 

I also made comments on the Git pull requests and included relevant screenshots of the testing steps from Insomnia. My project has evolved from the initial ER diagram as I identified modifications that would enhance the API's functionality. Using Trello, I implemented checklists to ensure I thoroughly tested all endpoints. Additionally, adding time estimates and labels helped me monitor my progress and ensure that I could complete the project on schedule.

Bellow, I have attached some screenshots of my trello board and git commits.

## Git Pull requests

![First pull request](./docs/git/models_schemas_pullrequest.png)

![Auth pull request](./docs/git/auth_pullrequest.png)

![Group pull request](./docs/git/group_controller_pullrequest.png)

![Group_logs pull request](./docs/git/group_logs_pullrequest.png)

![Log_controller pull request](./docs/git/log_controller_pullrequest.png)

![Marathon pull request](./docs/git/marathon_controller_pullrequest.png)

![Workout pull request](./docs/git/workout_pullrequest.png)

## Trello

![Trello progress 1](./docs/trello/trello1.png)

![Trello progress 2](./docs/trello/trello2.png)

![Trello progress 3](./docs/trello/trello3.png)

![Trello progress 4](./docs/trello/trello4.png)

![Trello progress 5](./docs/trello/trello5.png)

![Trello progress 6](./docs/trello/trello6.png)

![Trello progress 7](./docs/trello/trello7.png)

[Link to Git hub T2A2 repo](https://github.com/Jessicavazm/JessicaVaz_T2A2.git)

[Link to Trello Board](https://trello.com/b/rwRXu3bo)


## R3 

- Virtual environment
Virtual environment is used to isolate the project to not interfere with other projects.
This is the first step when we start on the API project. To set up the virtual environment we navigate to our source folder and type: *python3 -m venv venv*. The name `venv` is a convention name used for virtual environments. To activate the virtual environment we navigate to our source folder and type *source venv/bin/activate*. Now we can start getting all the necessary dependencies to build the API project.

- Python-dot-env
This package is used to help setting up the environment variables that are used to keep sensitive data such as username, password secure. In our project, the environment variables holds the information from database URL and JWT secret key. This file is excluded from the git, but in order for our project to work we need a way to tell other developers or testers they have to set up the environment variables on their end. In this project this has been done through the `.env.example` file which it contains the variables examples. Bellow is the example of the .env.example file.

### Sample of the variables that needs to be defined
	DATABASE_URL = 
	JWT_SECRET_KEY = 

- Flask
Flask is lightweight yet powerful Python based framework that depends on Werkzeug (WSGI library), Jinja (for rendering the pages on server) and Click (for Flask commands lines and custom commands). All dependencies are installed automatically when you instal Flask.

- PostgreSQL
It's an open-source relational database management system. It's consist of tables (it stores the data into rows and columns), schemas (it organise and manages DB objects). Additionally, it's a very versatile system that supports a wide range of data types and integrates with different programming languages.

- Psycopg2 
It works as the driver that connects the API to the DB. It allows your Python applications to connect to and interact with a PostgreSQL database. 

- SQLalchemy 
It's an Object-Relational Mapping (ORM), that converts Python objects(classes) into database tables. It also allows SQL queries using Python language.

- Marshmallow 
It helps flask to read data from/ to the database. It's a Python library used for serialisation and deserialisation of data. 
 - Serialise (convert Python objects into JSON).
 - Deserialise (convert input data into Python objects).

- Marshmallow_sqlalchemy 
Extension that facilitates integration between marshmallow and sqlalchemy, it generates schemas based on sqlalchemy models that is used for data serialization/deserialization.

- Sqlalchemy.exc
It handles exception errors that might arise when dealing with database operations. It includes: data integrity errors, data errors.

- Marshmallow.exceptions
Used to handle validations errors when serializing and deserializing data.
 
- Flask_bcrypt  
Used for handling sensitive data and password encryption.

- Flask_jwt_extended 
Flask extension used for authentication methods by creating tokens.

- JWTManager
It helps in the process of token decoding and verification.

- Functools
It's used when creating decorators, it allows a function to take another function as a parameter by using the wraps method.

- OS
It's part of Python standard library, it's used to fetch environment variables from .env file and import into main.py file. It connects with the operating system.

- Datetime
To display time in attributes that requires time information.

- Marshmallow.validate
Built-in validators that can be used to enforce data validation. These validations are placed in the schemas. It can be used on name, email, password, one of (it's used to ensure that a field's value is one of a specified set of acceptable choices).


## R4 

Postgresql serves as open-source relational database management system (RDBMS) that enables users to store, manage, and retrieve data efficiently and securely. It's stores data in a practical and easy to manage way. Data is stored in DB using tables where tables are the entities, attributes are the columns and objects are the rows.

It ensures data maintain it's integrity by placing constraints in tables (primary and foreign keys, unique and not null rules). Users are able to perform queries using SQL, PostgreSQL, programming languages.

- By adhering to the ACID principles (Atomicity, Consistency, Isolation, and Durability), the database system ensures that all data is processed and stored in a very reliable way.
- Postgresql complies with SQL standards which helps when migrating from other SQL databases.
- Flexibility: PostgreSQL can either be used as relation db system or non relational (NoSQL) for JSON data storage and query.
- Postgres DB system is compatible with most computer operating systems such as Linux, Windows, MacOS, BSD and Solaris.
- It's an open source and free of charge application.
- Multi-Version concurrency Control allows multiple data to be processed simultaneously without interfering with each other.
- Accepts Primitives data, Structured data such as Date/time, Arrays, Range, JSON, JSONB, XML, Geometry Data and it also allows you to custom your own data(composite and custom types).
- PostgreSQL supports many different types of authentication such as GSSAPI, SSPI, LDAP, SCRAM-SHA-256 and Certificate. Pgcrypto extension can also be used in PostgreSQL to perform hashing and encryption to handle sensitive data and ensure data security.

## Functionalities 
- Data Integrity and Constraints
 - Primary Keys: Unique identifiers in each table
 - Foreign Keys: Maintain referential integrity between related tables.
 - Constraints: ensure rules on attributes.

- Table partitioning
 - Useful when it comes to table management and readability. This function slipt larger table in smaller tables but the table is still managed as one piece.

- Role Management: 
 - Create and manage user roles and permissions.

- Data Definition Language (DDL)
 - Create tables: Define new tables with specific columns, data types, and constraints.
 - Alter Tables: Modify existing tables to add, remove, or change columns and constraints.
 - Drop Tables: Remove tables and their data from the DB

- Data Manipulation Language (DML)
 - Insert Data: Add new data using the INSERT statement.
 - Update Data: Modify existing data using the UPDATE statement.
 - Deleting Data: Remove data using the DELETE statement.
 - Selecting Data: Retrieve data from tables using the SELECT statement combined with a condition.

### Drawbacks:

- Database software does not carry liability for damages or offers warranty of any kind.
- Data migrating/ and software updates can be complex/slow.
- Performance can be considered slower than SQL Server and MySQL.

References: Coder academy workbook assignment T2A1-A - Jessica Vaz


## R5

### Purpose
The purpose of SQLAlchemy is to allow interaction with the database using Python objects and classes. Instead of writing SQL queries to create, add, or remove data, SQLAlchemy simplifies these tasks and helps reduce errors. It provides a high-level abstraction that enables developers to define their database schema using Python classes and manage relationships between different data models easily.
SQLAlchemy also supports queries using filtering, sorting, and joining of data through Python language.
Overall, SQLAlchemy provides a great framework for building applications that require reliable and efficient data management.


### Features
- SQLalchemy allows integration with different DB systems
- Easy DB migrations
- It allows DB queries in Python code
- Customized how data is handled
- SQLAlchemy has a large community and many resources available online

### Functionalities  

- Db.relationship: SQLAlchemy allows database relationships to be set in when defining the tables, the relationship demonstrate how all the tables connect between each other. This is very important since in a relational DB, all the data is connected through the tables. 

- Back_populates: establishes a two-way relationship. It allows access to related records from both sides of the relationship.

- Cascading: SQLAlchemy allows cascading operations. If you delete record in one table, it will automatically deleted from the related table.

- Allows queries using Python syntax.

### Example of db.relationship, back-populates, and cascading functionalities in User model

	class User(db.Model):
		# Name of the table
		__tablename__ = "users"

		# Attributes
		id = db.Column(db.Integer, primary_key=True)
		name = db.Column(db.String(30), nullable=False)
		email = db.Column(db.String(50), nullable=False, unique=True)
		password = db.Column(db.String, nullable=False)
		is_admin = db.Column(db.Boolean, default=False)
    

		# Define bidirectional relationships with workouts, group_logs and groups tables.
		# Cascade to delete workouts and group if user is deleted
		workouts = db.relationship("Workout", back_populates = "user", cascade="all, delete")
		group_logs = db.relationship("GroupLog", back_populates="user", cascade="all, delete")
		group_created = db.relationship("Group", back_populates = "group_admin", cascade="all, delete")


### Query using filter_by and order_by code to query specific user workout logs
	
	@workout_bp.route("/")
	@jwt_required()
	def get_all_workouts():
		# Get the current user's identity from the JWT token
		current_user = get_jwt_identity()

		# Create and execute statement, filter by user's ID, order by desc date
		stmt = db.select(Workout).filter_by(user_id=current_user).order_by(Workout.date.desc())
		workouts = list(db.session.scalars(stmt))
		
		if workouts:
			# Serialize data using workouts_schema
			return workouts_schema.dump(workouts), 200
		else:
			# Else return error msg
			return {"Error": "No workout logs to display for this user."}, 400


## R6 

Important: As I continued with my project, I realized I needed to add an extra table to my diagram to store entries from users in groups. This new change will allow me to organize user entries in groups more effectively.

I have also added a new foreign key in the groups table for the created_by attribute to indicate which admin created the group, allowing my queries to be executed more effectively. I have made some changes from the previously submitted ER diagram to improve the functionality of my API. I have discussed these changes with Aamod to get approval.

![ER diagram](./docs/Marathon_API.drawio.png)

### Models:

#### User: 
	- id: PK
	- name: not null
	- email: not null
	- password: not null
	- is_admin: default=False

#### Workout
	- id: PK
	- title: not null
	- date_created: not null
	_ distance_kms: not null
	- calories_burnt
	- user_id (FK referencing user who created workout log)

#### Groups
	id: PK
	name: not null
	date_created: date
	created_by: user_id (FK referencing the admin who created the group)

#### Group_logs
	id: PK
	date_created: date
	user_id: FK (referencing the user who entered the group), not null
	group_id: FK (referencing the group the user entered), not null

#### Marathons
	id: PK
	name: not null
	event_date: not null
	location: not null
	distance_kms: not null

#### Marathons_logs
	id: not null
	date_created: not null
	group_id: FK(referencing the group who entered the marathon event), not null
	marathon_id: FK (referencing the what marathon event the group entered), not null

### Relationships:
	- User can log many workout logs
	- Workout log belongs to one user
	- User can be part of many groups
	- A group can have many users
	- A group can be created by only one user
	- Groups can enter many marathons
	- Marathons can be entered by many groups


## R7 

## User

### Attributes
Nullable constraint to ensure data input and unique=True to ensure email is unique

	- id = db.Column(db.Integer, primary_key=True)
	- name = db.Column(db.String(30), nullable=False)
	- email = db.Column(db.String(50), nullable=False, unique=True)
	- password = db.Column(db.String, nullable=False)
	- is_admin = db.Column(db.Boolean, default=False)
    
### Relationship
	Bi-directional relationship with workouts, group_logs and group_created to ensure data is shared across 
	requested tables.

### User schema
Validation on user's name, email, password.
- name: Name must be between 2 and 30 characters in length. Name must start with an uppercase letter and contain only letters.

- email: Email must be between 5 and 50 characters in length. The email cannot have consecutive dots, must have a local part, a non-empty domain name, and a top-level domain containing at least two letters. Valid characters include letters, numbers, underscore, period, percent sign, plus sign, and hyphen.

- password: Password must be a minimum of 6 characters and maximum of 20 characters. Password must contain one upper case letter, one digit and one special character.

### Class meta
    class Meta:
        fields = ["id", "name", "email", "password", "is_admin", "workouts", "group_logs", "group_created"]
        ordered = True 


## Workout

### Attributes

- id = db.Column(db.Integer, primary_key=True)
- title = db.Column(db.String, nullable=False) 
- date =db.Column(db.Date, default=date.today)
- distance_kms = db.Column(db.Integer, nullable=False)
- calories_burnt = db.Column(db.Integer)

### FK to reference 'users' table
	- user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

### Bidirectional relationships with 'users' table
	user = db.relationship("User", back_populates = "workouts")

## Workout Schema

- Title validation using a constant
	title = fields.String(required=True, validate=OneOf(VALID_STATUSES))
    
- Class Meta:
	fields = ["id", "title", "date", "distance_kms", "calories_burnt", "user"]

## Group

### Attributes
	- id = db.Column(db.Integer, primary_key=True)
	- name = db.Column(db.String(30), nullable=False)
	- date_created = db.Column(db.Date, default=date.today)
	- created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)

### Bidirectional relationships with group_admin creator, groups_logs and marathons_logs
    - group_admin = db.relationship("User", back_populates= "group_created")

    - group_logs = db.relationship("GroupLog", back_populates= "group", cascade="all, delete")

    - marathon_logs = db.relationship("MarathonLog", back_populates= "group", cascade="all, delete")

### Group schema

- Validation for attribute 'name':
	- Name must be between 4 and 30 characters in length.Name must start with an uppercase letter and contain only letters."

### Class Meta
	fields = ["id", "name", "date_created", "created_by", "group_admin", "group_logs", "marathon_logs"]
      
## Group_logs

### Attributes

	- id = db.Column(db.Integer, primary_key=True)
	- entry_created = db.Column(db.Date, default=date.today) 

### Foreign keys to reference both 'users' and 'groups' tables
- user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

- group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False)

### Bi directional relationships with 'users' and 'groups' tables
	user = db.relationship("User", back_populates="group_logs")

	group = db.relationship("Group", back_populates="group_logs")

### Group_log schema
class Meta:
    fields = ["id", "entry_created", "user", "group"]


## Marathon table

### Attributes

	- id = db.Column(db.Integer, primary_key=True)
	- name = db.Column(db.String(30), nullable=False)
	- event_date = db.Column(db.Date, nullable=False)
	- location = db.Column(db.String(50), nullable=False)
	- distance_kms = db.Column(db.Integer, nullable=False)
		
### Bidirectional relationships with 'marathon_logs' table
- Cascade to delete marathon_logs and group if marathon is deleted.

    marathon_logs = db.relationship("MarathonLog", back_populates="marathon", cascade="all, delete")

### Schemas
- Validation for 'name' and 'location'
    name = Name must be between 4 and 30 characters in length. Name must start with an uppercase letter and contain only letters."
    
- Validation for attribute 'location'
    Allows letter, numbers, spaces, apostrophes and commas. Location must be between 10 and 50 characters in length.

- Class Meta:
    fields = ["id", "name", "event_date", "location", "distance_kms", "marathon_logs"]


## Marathon_logs table

### Attributes
	- id = db.Column(db.Integer, primary_key=True)
	- entry_created = db.Column(db.Date, default=date.today) 

### Foreign keys to reference both 'groups' and 'marathons' tables
	- group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False)

	- marathon_id = db.Column(db.Integer, db.ForeignKey("marathons.id"), nullable=False)

### Bidirectional relationships with 'groups' and 'marathons' tables
	- group = db.relationship("Group", back_populates="marathon_logs")
	
	- marathon = db.relationship("Marathon", back_populates="marathon_logs")

### Marathon_logs Schema
- class Meta:
    fields = ["id", "entry_created", "group", "marathon"]


# R8 

## Users endpoints

### Route for users to register:
	- Route: localhost:8080/auth/register
	- Method: POST
	- Body required : Name, email and password and is_admin. 
	- Requirements for name, email and password.

### Example of body of request:
	{
	"name": "Jess",
	"email": "jess@email.com",
	"password": "Brazil1."
	}

### Response
When request is successful, user will see their info displayed apart from password. Http response will be 201 created. Example:

	{
	"id": 4,
	"name": "Jess",
	"email": "Jess@email.com",
	"is_admin": false,
	"workouts": [],
	"group_logs": [],
	"group_created": {}
	}

### Possible error msgs users can receive when registering:
- Unique email violation: “error": "Email address must be unique
- Name violation: error": "An unexpected error has occurred {'name': ['Name must be between 2 and 30 characters in length.']}"
- Email violation: error": "An unexpected error has occurred {'email': ['Invalid email format: The email cannot have consecutive dots, must have a local part, a non-empty domain name, and a top-level domain containing at least two letters. Valid characters include letters, numbers, underscore, period, percent sign, plus sign, and hyphen.']}"
- Password violation: "error": "An unexpected error has occurred {'password': ['Invalid password format. Password must contain one upper case letter, one digit and one special character.']}"
- Missing fields violation: "error": "An unexpected error has occurred {'password': ['Missing data for required field.']}"

![Successful user sign up](./docs/user/user_signup/user_registration_successful.png)

![Email violation](./docs/user/user_signup/user_unique_email_violation.png)

![Missing fields violation](./docs/user/user_signup/missing_fields_violation.png)

![Name violation](./docs/user/user_signup/name_violation.png)

![Password violation](./docs/user/user_signup/user_name_password_violations.png)

![Unique email violation](./docs/user/user_signup/user_unique_email_violation.png)


### Route for user login
	- Route: localhost:8080/auth/login
	- Method: POST
	- Body request: Email and password

### Example of body of request:

	{
	"email": "jess@email.com",
	"password": "Brazil1."
	}

### Response
When a user logs in, the application will return the user's email and token. Example of a response body:
	
	"email": "jess@email.com",
	"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyNzUwODE1OCwianRpIjoiYjkyYWYwZTYtNjRkYS00YTQ2LThiY2QtY2I2Yzk5OGMyMDRlIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjQiLCJuYmYiOjE3Mjc1MDgxNTgsImNzcmYiOiIwNDAxYmUxMi1jNmI2LTQwMzMtODU4Ny1mMThhOTk4NTAzZDQiLCJleHAiOjE3Mjc1OTQ1NTh9 4E2n4B6g-22o-U_QKWs0MXsBcEt7NOVLLi_-O9B7CxE"
	

### Possible error msgs users can receive when logging in:
- Invalid credentials: "error": "Invalid credentials"
- Missing fields: "error": "Email and password are required.”

![Invalid credentials](./docs/user/user_login/invalid_login_credentials.png)

![Missing fields violation](./docs/user/user_login/missing_fields.png)


### Route for user to update their details
	- Route: localhost:8080/auth/login
	- Method: POST
	- Body request: Name, email or password.
	- JWT token is required in the authorisation header

### Example of body of request:
	“name”: “Jessica”,
	"email": "jess@email.com"

### Response
When request is successful, the new updated details will be displayed back to users, apart from password. Example:

	{
	"id": 4,
	"name": "Jessica Vaz",
	"email": "jessica.vaz@email.com",
	"is_admin": false,
	"workouts": [],
	"group_logs": [],
	"group_created": {}
	}

### Possible error messages: 
- Unique email error msg. 
- Email, password and name violations.

![Successful user info update](./docs/user/user_info_update/user_details_update.png)

![unique email violation](./docs/user/user_info_update/email_update_unique_violation.png)

![password violation](./docs/user/user_info_update/password_update_violation.png)


### Delete user route
Users can delete themselves and admin users can delete regular users.

	- Route: localhost:8080/auth/users/<user_id>
	- Parameter: user_id. 
	- Method: Delete
	- JWT is required in the authorisation header

### Response 

When request is successful, it will display an acknowledgement message back to user. Example:

	{
	"message": "Jess with ID number 6 has been successfully deleted."	
	}

![Successful user delete](./docs/user/delete_user/successful_200.png)

![403 error user delete route](./docs/user/delete_user/403_error.png)

![404 error user delete route](./docs/user/delete_user/404_error.png)


## Workouts endpoints

Only the user can see, update and delete their workout sessions.

### Route to see workout logs
	- Route: localhost:8080/workouts/
	- Method: GET
	- JWT token is required in the authorisation header

### Response
When request is successful user will see all workouts sessions logged in the app. Example:

	{
	"id": 1,
	"title": "Outside run",
	"date": "2024-09-28",
	"distance_kms": 10,
	"calories_burnt": 235,
	"user": {
		"id": 1,
		"name": "User A"
	}
	},
	{
	"id": 3,
	"title": "Treadmill",
	"date": "2024-09-28",
	"distance_kms": 4,
	"calories_burnt": 500,
	"user": {
		"id": 1,
		"name": "User A"
	}
	}

### Possible errors: 
- Not authenticated user.
- User hasn’t logged a workout yet, a personalised error msg will be displayed back to user. 

![See all workouts](./docs/workout/see_workouts/get_all_workouts_200.png)

![No workout to display](./docs/workout/see_workouts/no_workouts.png)


### Route to see a specific workout log
	- Route: localhost:8080/workouts/<workout_id>
	- Method: GET
	- Parameter: <workout_id>
	- JWT token is required in the authorisation header

### Response
When the request is successful, the specific workout will be displayed to user. Example:
	
	"id": 1,
	"title": "Outside run",
	"date": "2024-09-28",
	"distance_kms": 10,
	"calories_burnt": 235,
	"user": {
		"id": 1,
		"name": "User A"
	}

### Possible errors: 
- Not authenticated user.
- Not found workout log, personalised msg will be displayed back to user.

![Display specific workout log](./docs/workout/see_workouts/get_specific_workout.png)

![Workout not found](./docs/workout/see_workouts/workout_not_found.png)


### Route to log a workout session
	- Route: localhost:8080/workouts/
	- Method: POST
	- Body required: title, distance_kms, calories_burnt(Optional).
	- JWT token is required in the authorisation header.

### Body of request eg:
	{
	"title": "Outside run",
	"distance_kms":"20"
	}

### Response
When request is successful, the log will be displayed back to the user. Example:

	"id": 15,
	"title": "Outside run",
	"date": "2024-09-28",
	"distance_kms": 20,
	"calories_burnt": null,
	"user": {
		"id": 7,
		"name": "Jess"
	}

### Possible errors: 
- Integrity violation, missing distance_kms. 
- Data error, wrong data input for distance_kms and calories_burnt. 
- Data violation for title attribute, title received a different input from one of the allowed options.

![Create workout created](./docs/workout/create_workout/workout_201.png)

![Create workout, missing fields violation](./docs/workout/create_workout/missing_field_violation.png)

![Create workout, title violation](./docs/workout/create_workout/title_violation.png)

![Create workout, data type violation](./docs/workout/create_workout/INT_values_violations.png)


### Route to update a workout log
	- Route: localhost:8080/workouts/<workout_id>
	- Method: PATCH/ PUT
	- Parameter: <workout_id>
	- Required body: Attribute user wish to update (title, distance_kms or calories_burnt).
	- JWT token is required in the authorisation header.

### Body of request eg:
	{
	"title": "Outside walk",
	"distance_kms":"5"
	}

### Response: 
When request is successful, the new update log will be displayed back to user. Example:

	"id": 15,
	"title": "Outside walk",
	"date": "2024-09-28",
	"distance_kms": 20,
	"calories_burnt": 550,
	"user": {
		"id": 7,
		"name": "Jess"
	}

### Possible errors:
- Workout not found 
- Data violations

![Workout created](./docs/workout/update_workout/update_successful_200.png)

![Workout data input violation](./docs/workout/update_workout/data_type_violation.png.png)

![User not authorised](./docs/workout/update_workout/not_authorised_403.png)

![Workout log not found](./docs/workout/update_workout/workout_not_found_404.png)


### Route to delete a specific workout log
	- Route: localhost:8080/workouts/<workout_id>
	- Method: DELETE
	- Parameter: <workout_id>
	- JWT token is required in the authorisation header.

### Response: 
When request is successful, an acknowledgment msg will be returned to user. Example:
	
	"message": "Workout 4 has been deleted successfully!"	
	

### Possible errors: 
- Workout not found
- Not authorised user

![Workout deleted](./docs/workout/delete_workout/successful_delete_workout.png)

![Not authorised user](./docs/workout/delete_workout/not_authorised_403.png)

![Workout not found](./docs/workout/delete_workout/workout_not_found_404.png)


## Groups endpoints

## Routes users to see created groups
- Route: localhost:8080/groups
- Method: GET
- JWT token is required in the authorisation header.

### Response: 
When request is successful, the groups will be displayed back to user. Example:

	{
	"id": 1,
	"name": "Australian Team",
	"date_created": "2024-09-29",
	"created_by": 1,
	"group_admin": {
		"name": "User A"
	},
	"group_logs": [],
	"marathon_logs": []
	},
	{
	"id": 2,
	"name": "Coder Team",
	"date_created": "2024-09-29",
	"created_by": 2,
	"group_admin": {
		"name": "User B"
	},
	"group_logs": [],
	"marathon_logs": []
	}


### Route to see a specific group
- Route: localhost:8080/groups/<group_id>
- Method: GET
- JWT token is required in the authorisation header.

### Response: 
When request is successful, the group will be displayed back to user. Example:

	{
	"id": 2,
	"name": "Coder Team",
	"date_created": "2024-09-29",
	"created_by": 2,
	"group_admin": {
		"name": "User B"
	}
	}
	
### Possible errors:
- User not authenticated
- Group or groups doesn't exist yet

![Missing auth](./docs/group/see_groups/missing_auth.png)

![Get all groups](./docs/group/see_groups/see_groups_200.png)

![Get one specific group](./docs/group/see_groups/see_specific_group.png)

![Group not found](./docs/group/see_groups/not_found_group.png)


### Create group (only admins allowed, one group per admin)

- Route: localhost:8080/groups/register
- Method: POST
- Requested body: Name
- JWT token is required in the authorisation header.

### Response: 
When request is successful, the created group will be displayed back to admin user. Example:

	{
	"id": 5,
	"name": "Coder Team",
	"date_created": "2024-09-29",
	"created_by": 1,
	"group_admin": {
		"name": "User A"
	},
	"group_logs": [],
	"marathon_logs": []
	}

### Possible errors:
- Not admin user
- Admin already has created one group
- Name Violation

![Group created](./docs/group/create_groups/group_register.png)

![Group name violation](./docs/group/create_groups/name_violation.png)

![Admin already created a group violation](./docs/group/create_groups/only_1_group_validation.png)


### Route to update groups info (only admin allowed)

- Route: localhost:8080/groups/<group_id>
- Method: POST
- Parameter: <group_id>
- Requested body: Name
- JWT token is required in the authorisation header.

## Body of request:

	{
	"name": "Girls Run"
	}

### Response: 

When request is successful, the updated group will be displayed back to admin user. Example:
	
	"id": 3,
	"name": "Girls Run",
	"date_created": "2024-09-29",
	"created_by": 1,
	"group_admin": {
		"name": "User A"
	},
	"group_logs": [],
	"marathon_logs": []
	

### Possible errors:
- Not authorised user
- Not authorised admin (admins can only update their own group)
- Group name violations

![Group updated](./docs/group/group_update_info/updated_details_200.png)

![Not authorised user](./docs/group/group_update_info/not_authorised_user.png)

![Not authorised admin](./docs/group/group_update_info/not_authorised_admin.png)


### Route to delete a group (only admin allowed)

- Route: localhost:8080/groups/<group_id>
- Method: DELETE
- Parameter: <group_id>
- JWT token is required in the authorisation header.

### Response: 

When request is successful, an acknowledgment msg will be displayed back to the admin user. Example:
	
	"message": "Group 4 has been deleted successfully!"
	

### Possible errors:
- Group not found
- Not authorised user
- Not authorised admin (admins can only delete their own group)

![Delete successful](./docs/group/delete_group/delete_successful.png)

![Group not found](./docs/group/delete_group/group_not_found.png)

![Not authorised admin](./docs/group/delete_group/admin_not_authorised.png)

![Not authorised user](./docs/group/delete_group/regular_member_not_authorised.png)


### Route for regular members to sign up to a group
- Route: localhost:8080/groups/<group_id>/join
- Method: POST
- Parameter: <group_id>
- JWT token is required in the authorisation header.

### Response

When request is successful, an acknowledgment msg will be displayed back to user. Example:
	
	"message": "Luke is officially part of the group named Group A."
	

### Possible errors:
- Group doesn't exist
- Already a member of the requested group
- User not authenticated
- Admin one group violation

![Sign up successful](./docs/group/group_signup/sign_up_201.png)

![Group not found](./docs/group/group_signup/group_not_found.png)

![Group not found](./docs/group/group_signup/admin_only_allowed_1group.png)

![Already member of the group](./docs/group/group_signup/already_member.png)


### Route for regular members to unsubscribe from a group
- Route: localhost:8080/groups/<group_id>/unsubscribe
- Method: DELETE
- Parameter: <group_id>
- JWT token is required in the authorisation header.

### Response

When request is successful, an acknowledgment msg will be displayed back to user. Example:
	
	"message": "You have successfully left the group named Group B."
	

### Possible errors:
- Group not found
- Not a group member
- Admin cannot leave their own group

![Leave group request successful](./docs/group/group_signup/leave_group_successful.png)

![Group not found](./docs/group/group_signup/delete_group_not_found.png)

![Not a member of the group](./docs/group/group_signup/not_member.png)

![Admin cannot leave group violation](./docs/group/group_signup/delete_group_admin_violation.png)


## Marathons routes


## Routes users to see marathons events
- Route: localhost:8080/marathons
- Method: GET
- JWT token is required in the authorisation header.

### Response: 
When request is successful, the groups will be displayed back to user. Example:

	{
	"id": 2,
	"name": "Coder Run",
	"event_date": "2025-10-08",
	"location": "Melbourne",
	"distance_kms": 20,
	"marathon_logs": 
		{
			"id": 1,
			"entry_created": "2024-09-29"
		}
	}
	{
	"id": 1,
	"name": "Marathon A",
	"event_date": "2026-12-12",
	"location": "Gold Coast",
	"distance_kms": 10,
	"marathon_logs": 
		{
			"id": 2,
			"entry_created": "2024-09-29"
		}
	}

### Possible errors:
- Marathons has not been created yet
- Not authenticated user


### Route to see a specific marathon
- Route: localhost:8080/marathons/<marathon_id>
- Method: GET
- JWT token is required in the authorisation header.

### Response: 
When request is successful, the requested marathon will be displayed back to user. Example:

	{
	"id": 1,
	"name": "Marathon A",
	"event_date": "2026-12-12",
	"location": "Gold Coast",
	"distance_kms": 10,
	"marathon_logs": 
		{
			"id": 2,
			"entry_created": "2024-09-29"
		}
	}
	
- Specific marathon does not exist
- Not authenticated user

![See all marathons](./docs/marathons/get_marathons/see_all_marathons_200.png)

![See specific marathon](./docs/marathons/get_marathons/see_specific_marathon.png)

![Marathon not found](./docs/marathons/get_marathons/not_found.png)


### Route to create marathons (only admin allowed, they can create as many as they wish).
- Route: localhost:8080/marathons/register
- Method: POST
- Body of request: Name, event_date, location and distance_kms.
- JWT token is required in the authorisation header.

### Example of body of request
	{
	"name": "Coder Marathon",
	"event_date": "2025-12-01",
	"location": "12 O'Connor, Melbourne",
	"distance_kms": "15"	
	}

### Response

When request is successful, the marathon event will be displayed back to user. Example:
	
	"id": 4,
	"name": "Coder Marathon",
	"event_date": "2025-12-01",
	"location": "12 O'Connor, Melbourne",
	"distance_kms": 15,
	"marathon_logs": []
	

### Possible errors:
- Not authenticated user
- Not admin
- Name, event date, location, and distance violations

![Created marathon](./docs/marathons/create_marathons/marathon_created_201.png)

![Date violations](./docs/marathons/create_marathons/invalid_date.png)

![Missing fields](./docs/marathons/create_marathons/missing_fields.png)

![Invalid date](./docs/marathons/create_marathons/past_date_violation.png)


### Route to update marathons events, (only admins allowed, all admins can edit info related to all marathon events.)
- Route: localhost:8080/marathons/register
- Method: POST
- Parameter: <marathon_id>
- Body of request: Attributes admin wants to update, it can include: name, event date, location and distance.
- JWT token is required in the authorisation header.

### Example of a body of request:
	{
	"location" : "Opera house, Sydney"
	}

### Body of response
When request is successful, the new marathon info will be displayed back to admin user. Example:	
	
	"id": 4,
	"name": "Coder Marathon",
	"event_date": "2025-12-01",
	"location": "Opera house, Sydney",
	"distance_kms": 15,
	"marathon_logs": []

### Possible errors:
- Not authenticated user 
- Not admin
- Marathon does not exist
- Name, event date, location, and distance violations

![Updated successfully](./docs/marathons/update_marathons/update_successful.png)

![Invalid data type](./docs/marathons/update_marathons/invalid_data_type.png)

![Only admin allowed](./docs/marathons/update_marathons/only_admin.png)


### Route to delete marathons events, (only admins allowed, admins can delete all marathon events.)
- Route: localhost:8080/marathons/<marathon_id>
- Method: DELETE
- Parameter: <marathon_id>
- JWT token is required in the authorisation header.

### Response
When request is successful, an acknowledgment msg will be displayed back to admin user. Example:

	{
	"message": "Coder Marathon event has been deleted successfully!"
	}

### Possible errors:
- Not authenticated user
- Not admin
- Requested marathon event does not exist

![Only admin allowed](./docs/marathons//delete_marathons/deleted_successful.png)

![Marathon event not found](./docs/marathons/delete_marathons/not_found.png)


## Route to enrol groups in the marathons events, (only admins allowed, each admin can enrol their own group in the marathon events).
- Route: localhost:8080/marathons/<marathon_id>/signup
- Method: POST
- Parameter: <marathon_id>
- JWT token is required in the authorisation header.

### Response
When request is successful, the log entry containing group and marathon event information will be displayed back to the admin. Example:


	"id": 4,
	"entry_created": "2024-09-29",
	"group": {
		"id": 1,
		"name": "Group A",
		"date_created": "2024-09-29",
		"created_by": 1,
		"group_admin": {
			"name": "User A"
		},
		"group_logs": [
			{
				"id": 1,
				"entry_created": "2024-09-29",
				"user": {
					"id": 1,
					"name": "User A",
					"email": "admin_a@email.com"
				}
			}
		]
	},
	"marathon": {
		"id": 4,
		"name": "Coder Marathon",
		"event_date": "2025-12-01",
		"location": "12 O'Connor, Melbourne",
		"distance_kms": 15
	}


### Possible errors:
- Not authenticated user
- Not admin
- Already enrolled the group in the required marathon
- Admin hasn't created a group yet
- Marathon requested event doesn't exist

![Successful signup](./docs/marathons/marathon_signups/sign_up_201.png)

![Already joined error](./docs/marathons/marathon_signups/already_joined.png)

![Only admin allowed](./docs/marathons/marathon_signups/signup_only_admin.png)


## Route to remove the group from marathon event(only admin can perform this task, and they are only allowed to remove their own group)
- Route: localhost:8080/<marathon_id>/logs/<log_id>
- Method: DELETE
- Parameter: <marathon_id>, <log_id>
- JWT token is required in the authorisation header.

### Response
When request is successful, an acknowledgment msg will be sent back to admin. Example:
	
	"message": "Group A has been successfully removed from Marathon B event."


### Possible errors:
- Not authenticated user
- Not the admin who created the group
- Group hasn't enrolled for that specific marathon event

![Only admin allowed](./docs/marathons/marathon_signups/removed_log_200.png)

![Not authorised admin](./docs/marathons/marathon_signups/delete_log_not_auth.png)

![Log not found](./docs/marathons/marathon_signups/log_not_found.png)



