drop table if exists associate_batches;
drop table if exists trainer_batches;
drop table if exists notes;
drop table if exists associates;
drop table if exists batches;


create table if not exists trainers (
id serial primary key,
email varchar(50) not null,
first_name varchar(50) not null,
last_name varchar(50) not null,
admin bool not null
);

create table if not exists batches(
id serial primary key,
start_date bigint not null,
end_date bigint not null,
"name" varchar (50) not null,
training_track varchar(50)
);


create table if not exists trainer_batches(
trainer_id int not null,
batch_id int not null,
start_date bigint not null,
end_date bigint,
"role" varchar(50) not null,

constraint fk_trainer_batch foreign key (batch_id) references batches(id) on delete cascade,
constraint fk_trainer foreign key (trainer_id) references trainers(id) on delete cascade
);

create table if not exists associates(
id serial primary key,
email varchar(50) not null,
first_name varchar(50) not null,
last_name varchar(50) not null
);

create table if not exists associate_batches (
associate_id int not null,
batch_id int not null,
"start_date" bigint not null,
end_date bigint,
training_status varchar(50),

constraint fk_associate_batch foreign key (batch_id) references batches(id) on delete cascade,
constraint fk_associate foreign key (associate_id) references associates(id) on delete cascade
);

create table if not exists notes (
id  int primary key generated always as identity,
batch_id int,
cont varchar(200),
associate_id int,
week_number  int,
constraint fk_notes_batches foreign key(batch_id) references batches(id),
constraint fk_notes_associates foreign key(associate_id) references associates(id)
);


