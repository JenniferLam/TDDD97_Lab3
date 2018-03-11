create table userprofile(
email char(50) primary key not null,
firstname char(50) not null,
familyname char(50) not null,
gender char(6) not null,
city char(50) not null,
country char(50) not null,
password char(8) not null
);

create table message(
toemail char(50) not null,
fromemail char(50) not null,
content char(100)
);


create table login(
email char(50) primary key not null,
token char(50) not null
);

insert into userprofile (email, firstname, familyname, gender, city, country, password)
values ("abc@abc", "abc", "abc", "Female", "HK", "HK", "abcd1234");	


insert into userprofile (email, firstname, familyname, gender, city, country, password)
values ("def@def", "def", "def", "Female", "HK", "HK", "abcd1234");	


insert into message (toemail, fromemail, content)
values ("abc@abc","def@def", "Hello World");
insert into message (toemail, fromemail, content)
values ("abc@abc","def@def", "Hello World 2");
insert into message (toemail, fromemail, content)
values ("abc@abc","def@def", "Hello World 3");
insert into message (toemail, fromemail, content)
values ("abc@abc","abc@abc", "Hello World");
insert into message (toemail, fromemail, content)
values ("abc@abc","abc@abc", "Hello World 2");
insert into message (toemail, fromemail, content)
values ("abc@abc","abc@abc", "Hello World 3");
insert into message (toemail, fromemail, content)
values ("def@def","abc@abc", "Hello World");
insert into message (toemail, fromemail, content)
values ("def@def","abc@abc", "Hello World 2");
insert into message (toemail, fromemail, content)
values ("def@def","abc@abc", "Hello World 3");






