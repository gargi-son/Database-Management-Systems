/*Name:Gargi Sontakke
Gnumber:G01334018*/

CREATE TABLE Professors(
    Prof_SSN int,
    PRIMARY KEY(Prof_SSN)
);

INSERT INTO Professors (Prof_SSN)
VALUES('01237548');
INSERT INTO Professors(Prof_SSN)
VALUES('09347462');
INSERT INTO Professors (Prof_SSN)
VALUES('01863274');

CREATE TABLE Class(
    Prof_SSN int,
    Department Char(30) NOT NULL,
    Course_No Char(20) NOT NULL,
    PRIMARY KEY(Department,Course_No),
    FOREIGN KEY(Prof_SSN) REFERENCES Professors(Prof_SSN)
);

INSERT INTO Class(Department,Course_No)
VALUES('Computer Science','CS550');
INSERT INTO Class(Department,Course_No)
VALUES('DAEN','CS504');
INSERT INTO Class(Department,Course_No)
VALUES('CE','EC505');

CREATE TABLE Team(
    TeamID Char(10),
    Rating char(5),
    Prof_SSN int,
    PRIMARY KEY(TeamID),
    FOREIGN KEY (Prof_SSN) REFERENCES Professors(Prof_SSN)
);

INSERT INTO Team(TeamID,Rating,Prof_SSN)
VALUES('Team1','5','01237548');
INSERT INTO Team(TeamID,Rating,Prof_SSN)
VALUES ('Team2','4','09347462');
INSERT INTO Team(TeamID,Rating,Prof_SSN)
VALUES('Team3','3','01863274');

update team set rating = 3, prof_ssn = 01863274 where TeamID='Team3'


CREATE TABLE Class_Section(
    Section_ID Char(10),
    Department char(30),
    Course_No Char(20),
    TeamID Char(10),
    PRIMARY KEY(Section_ID,TeamID),
    FOREIGN KEY(TeamID) REFERENCES Team(TeamID),
    FOREIGN KEY(Department,Course_No) REFERENCES Class(Department,Course_No)
);

CREATE TABLE Student(
  Wait_Rank int,
  Grade char(5),
  Section_ID Char(10),
  Student_SSN int,
  TeamID Char(10),
  PRIMARY KEY(Student_SSN),
  FOREIGN KEY(Section_ID,TeamID) REFERENCES Class_Section(Section_ID,TeamID)
);

INSERT INTO Student(STUDENT_SSN, Wait_Rank,Grade)
VALUES('09857364','13','AB');
INSERT INTO Student(STUDENT_SSN, Wait_Rank,Grade)
VALUES('08475274','08','BB');
INSERT INTO Student(STUDENT_SSN, Wait_Rank,Grade)
VALUES('04725627','02','AA');

CREATE TABLE On_Team1 (
    Prof_SSN int,
    TeamID Char(10),
    PRIMARY KEY (Prof_SSN, TeamID),
    FOREIGN KEY (TeamID) REFERENCES Team (TeamID),
    FOREIGN KEY(Prof_SSN) REFERENCES Professors(Prof_SSN)
);

INSERT INTO On_Team1(Prof_SSN,TeamID)
VALUES('01237548','Team1');
INSERT INTO On_Team1(Prof_SSN,TeamID)
VALUES ('09347462','Team2');
INSERT INTO On_Team1(Prof_SSN,TeamID)
VALUES('01863274','Team3');

CREATE TABLE On_Team2 (
    Student_SSN int,
    TeamID Char(10),
    PRIMARY KEY (Student_SSN, TeamID),
    FOREIGN KEY (TeamID) REFERENCES Team(TeamID),
    FOREIGN KEY(Student_SSN) REFERENCES Student(Student_SSN)
);

CREATE TABLE GTA(
  Salary int,
  Student_SSN int,
  FOREIGN KEY (Student_SSN) REFERENCES Student(Student_SSN)
);

INSERT INTO GTA(Salary,Student_SSN)
VALUES('70000','09857364');
INSERT INTO GTA(Salary,Student_SSN)
VALUES ('80000','08475274');
INSERT INTO GTA(Salary,Student_SSN)
VALUES('90000','04725627');

CREATE TABLE Wait_for(
  Rank int,
  Student_SSN int,
  Section_ID Char(10),
  TeamID Char(10),
  PRIMARY KEY(Section_ID,TeamID),
  FOREIGN KEY(Student_SSN) REFERENCES Student(Student_SSN)
);

INSERT INTO Wait_for(Rank,Student_SSN,Section_ID,TeamID)
VALUES('1','09857364','S1','Team1');
INSERT INTO Wait_for(Rank,Student_SSN,Section_ID,TeamID)
VALUES ('2','08475274','S2','Team2');
INSERT INTO Wait_for(Rank,Student_SSN,Section_ID,TeamID)
VALUES('3','04725627','S3','Team3');

CREATE TABLE Take(
  Grade Char(5),
  Student_SSN int,
  Section_ID Char(10),
  TeamID Char(10),
  PRIMARY KEY(Section_ID,TeamID),
  FOREIGN KEY(Student_SSN) REFERENCES Student(Student_SSN)
);

INSERT INTO Take(Grade ,Student_SSN,Section_ID,TeamID)
VALUES('A1','09857364','S1','Team1');
INSERT INTO Take(Grade,Student_SSN,Section_ID,TeamID)
VALUES ('B1','08475274','S2','Team2');
INSERT INTO Take(Grade,Student_SSN,Section_ID,TeamID)
VALUES('C1','04725627','S3','Team3');
