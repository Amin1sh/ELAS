import React, {useEffect, useState} from 'react';
import Backend from "../../../assets/functions/Backend";
import "./smatch-styles.css";
import { NavLink } from "react-router-dom";
import Explore from "./components/Explore";

const SMATCHLogo = () => <img src="images/smatch.jpg" width="200px" height="150px" />;
const CogIcon = () => <img src="icons/cog.svg" />;
const HomeIcon = () => <img src="icons/home.svg" />;
const MessageIcon = () => <img src="icons/message.svg" />;
const ViewListIcon = () => <img src="icons/view-list.svg" />;
const ChartBarIcon = () => <img src="icons/chart-bar.svg" />;


const NavigationItem = ({ icon, to, badge }) => {
  return (
    <NavLink to={to} className={({ isActive }) => `fill-amber-500 ${isActive ? "w-12 h-12" : "w-8 h-8"} relative`}>
      {React.cloneElement(icon, { className: "w-full h-full" })}
      {badge ? (
        <span className="absolute -top-1 -right-1 inline-flex items-center px-1.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">{badge}</span>
      ) : <></>}
    </NavLink>
  );
}


const Smatch = () => {
  const [greeting, setGreeting] = useState("");

  useEffect(() => {
    Backend.get("/smatch/home").then((response) => {
      let res = response.data
      setGreeting(res)
    });
  })

  return (
    <div className="bg-slate-800 flex flex-col items-center justify-between min-h-screen">
      <div className="w-full max-w-4xl min-h-screen flex flex-col pb-24">
        
        <div className="flex flex-row item-center justify-center">
          <SMATCHLogo />
        </div>

        <div className="flex flex-row item-center justify-center">
          <Explore></Explore>
        </div>

        <div className="absolute bottom-0 inset-x-0 h-24 flex items-center justify-center">
          <div className="bg-gray-900 px-4 py-2 rounded-xl flex items-center gap-3">
            <NavigationItem icon={<CogIcon />} to="/smatch/settings" />
            <NavigationItem icon={<HomeIcon />} to="/smatch/" />
            <NavigationItem icon={<ViewListIcon />} to="/smatch/matches" />
            <NavigationItem icon={<MessageIcon />} to="/smatch/forum" />
            <NavigationItem icon={<ChartBarIcon />} to="/smatch/visualization" />
          </div>
        </div>
      </div>
    </div>
  );

}

export default Smatch;