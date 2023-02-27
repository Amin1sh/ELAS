import React from "react"
import { Link } from "react-router-dom";

import Title from "./Title";

export default function Explore() {
    let topics = ["Business","Design","Development","Finance & Accounting","Health & Fitness","IT & Software","Lifestyle","Marketing","Music","Office","Personal Development","Photography & Video","Productivity","Teaching & Academics",null];

    return (
        <div className="flex flex-col">
          <Title>
            Explore<br />Topics and Skills
          </Title>
    
          <div className="grid grid-cols-2 lg:grid-cols-3 gap-3 px-2 py-6">
            {topics ?
              topics.map((topic) => (
                <Link key={topic || "Other"} to={`/smatch/match/${encodeURIComponent(topic)}`} className="px-4 py-2 flex items-center justify-center text-center bg-gray-900 text-white rounded-full cursor-pointer">
                  { topic || "Other" }
                </Link>
              ))
              : <></>
            }
          </div>
        </div>
      )
}