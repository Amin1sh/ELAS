import React from "react";
import { useParams } from "react-router-dom";
import Title from "../Title/title";
import { useCourse } from "../hooks";
import style from "./coursepage-style";

export default function CoursePage() {
  const { id } = useParams();
  const course = useCourse(id);
  const classes = style();

  return course ? (
    <div className={`${classes['flex-1']} ${classes.flex} ${classes.flexCol}`}>
      <Title subtitle={course.provider}>
        {course.name}
      </Title>

      <div className={classes.gridContainer}>
        <Card title="Level" pageClasses={classes}><Level level={course.level} classes={classes} /></Card>
        <Card title="Instructor" pageClasses={classes}>{course.instructor}</Card>
        <Card title="Description" pageClasses={classes} classes={classes.descriptionItem}>
          <p>{course.description}</p>
        </Card>
        <Card title="Duration" pageClasses={classes} classes={classes.durationItem}>
          <p>
            {course.duration} Hours<br/>
          </p>
        </Card>
        <Card title="Price" pageClasses={classes} classes={classes.priceItem}>
          <p>${course.price}</p>
        </Card>

        <a href={course.link} target="_blank" className={classes.courseLink}>Click here to go to course</a>
      </div>
    </div>
  ) : <></>;
}

function Card({ title, classes, children, pageClasses }) {
  classes = classes || "";

  return (
    <div className={`${pageClasses.flex} ${pageClasses.flexCol} ${pageClasses.bgGray900} ${pageClasses.rounded30px} ${pageClasses.px6} ${pageClasses.pb6} ${pageClasses.pt4} ${pageClasses.gap4} ${classes}` }>
      <h2 className={`${pageClasses.textCenter} ${pageClasses.textLg} ${pageClasses.textAmber500}`}>{title}</h2>
      <div className={`${pageClasses.textWhite} ${pageClasses.textSm}`}>{children}</div>
    </div>
  );
}

function Level({ level, classes }) {
  return (
    <div className={classes.Levelcontainer}>
      <div className={`${level == "Beginner" || level == "Intermediate" || level == "Advanced" ? classes.bgActiveBar : classes['bg-gray-400']} ${classes['flex-1']} ${classes['h-1/3']}`}></div>
      <div className={`${level == "Intermediate" || level == "Advanced" ? classes.bgActiveBar : classes['bg-gray-400']} ${classes['flex-1']} ${classes['h-2/3']}`}></div>
      <div className={`${level == "Advanced" ? classes.bgActiveBar : classes['bg-gray-400']} ${classes['flex-1']} ${classes['h-full']}`}></div>
    </div>
  );
}