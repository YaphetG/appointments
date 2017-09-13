
drop table if exists tbl_appointments;
create table tbl_appointments(
  id integer primary key ,
  appointment_time datetime not null,
  description varchar(255) not null
);

INSERT INTO tbl_appointments (appointment_time,description) VALUES
  ('2017-09-16 4:20:00','dinner'),
  ('2017-09-14 8:20:00','meeting with a friend'),
  ('2017-09-12 4:20:00','coding challenge'),
  ('2017-09-26 4:20:00','Interview')
;
