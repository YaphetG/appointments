
drop table if exists tbl_appointments;
create table tbl_appointments(
  id int primary key,
  appointment_time datetime not null,
  description varchar(255) not null
);
