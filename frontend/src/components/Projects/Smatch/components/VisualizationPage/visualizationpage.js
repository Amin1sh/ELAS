import React, { useState, useEffect } from "react"
import { scaleOrdinal } from 'd3-scale';
import { schemeSpectral, schemeCategory10 } from 'd3-scale-chromatic';
import { BarChart, XAxis, YAxis, Tooltip, Legend, Bar, PieChart, Pie, Label, LabelList, ResponsiveContainer, Cell } from "recharts";

import Title from "../Title/title";
import { useVisualization } from "../hooks";
import { style } from './visualizationpage-style';

const colorsCategory = scaleOrdinal(schemeCategory10).range();
const colors = schemeSpectral[10];

const categories = [
  "instructors",
  "providers",
  "categories",
  "duration",
  "price",
  "terms"
];

export default function VisualizationPage() {
  const classes = style();
  const [selectedTab, setSelectedTab] = useState(categories[0]);

  return (
    <div className={`${classes['flex']} ${classes['flex-col']} ${classes['items-center']} ${classes['flex-1']}`}>
      <Title>
        Visualizations
      </Title>

      <div className={`${classes['flex']} ${classes['flex-col']} ${classes['mt-8']} ${classes['w-full']} ${classes['items-stretch']}`}>
        <Tabs selectedTab={selectedTab} setSelectedTab={setSelectedTab} classes={classes} />
        <TabContent category={selectedTab} classes={classes} />
      </div>
    </div>
  );
}

function Tabs({ selectedTab, setSelectedTab, classes }) {
  return (
    <ul className={classes.ulTabBox}>
      { categories.map((category) => (
        <TabItem classes={classes} key={category} value={category} isSelected={selectedTab == category} onClick={() => setSelectedTab(category)} />
      )) }
    </ul>
  );
}

function TabItem({ value, isSelected, onClick, classes }) {
  return (
    <li className={`${isSelected ? classes['bg-amber-700'] : classes['bg-gray-700']} ${classes.liItemCls}`} onClick={onClick}>
      { value.charAt(0).toUpperCase() + value.slice(1) }
    </li>
  );
}

function TabContent({ category, classes }) {
  return (
    <div className={classes.tabBox}>
      <TabVisualization category={category} classes={classes} />
    </div>
  );
}

function TabVisualization({ category, classes }) {
  switch (category) {
    case "instructors":
      return <InstructorsVisualization classes={classes} />;
    case "providers":
      return <ProvidersVisualization classes={classes} />;
    case "categories":
      return <CategoriesVisualization classes={classes} />;
    case "duration":
      return <DurationVisualization classes={classes} />;
    case "price":
      return <PriceVisualization classes={classes} />;
    case "terms":
      return <TermsVisualization classes={classes} />;
    default:
      return <></>;
  }
}

function InstructorsVisualization({ classes }) {
  const [dataCount, setDataCount] = useState(10);
  const data = useVisualization("instructors");

  return (
    <div className={classes['flex-center-items']}>
      <div className={classes.boxChart}>
        <label for="dataCount" className={classes.tabBoxLblCount}>Data count</label>
        <select id="dataCount" name="dataCount" value={dataCount} onChange={(e) => setDataCount(e.target.value)} className={classes.selectCount}>
          <option value={5}>5</option>
          <option value={10}>10</option>
          <option value={20}>20</option>
          <option value={40}>All</option>
        </select>
      </div>

      { data ?
        <BarChart
          width={600}
          height={800}
          data={dataCount == -1 ? data : data?.slice(0, dataCount)}
          margin={{ top: 5, right: 5, left: 5, bottom: 200 }}
        >
          
          <XAxis dataKey="instructor" interval={0} tick={{ angle: 90, fill: '#E5E7EB' }} tickMargin={100} />
          <YAxis dataKey={(v)=>parseInt(v.count)} tick={{ fill: '#E5E7EB' }} />
          <Tooltip />
          <Legend verticalAlign="top" height={36} />
          <Bar dataKey="count" fill="#0000" name="# courses by instructor">
            {
              data.map((entry, index) => (
                <Cell
                  key={`slice-${index}`}
                  fill={colors[index % 10]}
                  //fillOpacity={this.state.activeIndex === index ? 1 : 0.25}
                />
              ))
            }
          </Bar>
        </BarChart>
        : <></>
      }
    </div>
  );
}

function ProvidersVisualization({ classes }) {
  const data = useVisualization("providers");

  return (
    <div className={classes['flex-center-items']}>
      { data ?
        <BarChart
          width={600}
          height={600}
          data={data}
          margin={{ top: 5, right: 5, left: 5, bottom: 5 }}
        >
          
          <XAxis dataKey="provider" tick={{ fill: '#E5E7EB' }} />
          <YAxis dataKey={(v)=>parseInt(v.count)} tick={{ fill: '#E5E7EB' }} />
          <Tooltip />
          <Legend verticalAlign="top" height={36} />
          <Bar dataKey="count" fill="#F59E0B" label={{ fill: '#E5E7EB' }} name="# courses by provider">
            {
              data.map((entry, index) => (
                <Cell
                  key={`slice-${index}`}
                  fill={colors[index % 10]}
                  //fillOpacity={this.state.activeIndex === index ? 1 : 0.25}
                />
              ))
            }
          </Bar>
        </BarChart>
        : <></>
      }
    </div>
  );
}

function CategoriesVisualization({ classes }) {
  const data = useVisualization("categories");

  return (
    <div className={classes['flex-center-items']}>
      { data ?
        <BarChart
          width={600}
          height={800}
          data={data}
          margin={{ top: 5, right: 5, left: 5, bottom: 200 }}
        >
          
          <XAxis dataKey="category" interval={0} tick={{ angle: 90, fill: '#E5E7EB' }} tickMargin={100} />
          <YAxis dataKey={(v)=>parseInt(v.count)} tick={{ fill: '#E5E7EB' }} />
          <Tooltip />
          <Legend verticalAlign="top" height={36} />
          <Bar dataKey="count" fill="#F59E0B" name="# courses by category">
            {
              data.map((entry, index) => (
                <Cell
                  key={`slice-${index}`}
                  fill={colors[index % 10]}
                  //fillOpacity={this.state.activeIndex === index ? 1 : 0.25}
                />
              ))
            }
          </Bar>
        </BarChart>
        : <></>
      }
    </div>
  );
}

function DurationVisualization({ classes }) {
  const [nData, setNData] = useState(null);
  const [selectedLevel, setSelectedLevel] = useState("-");
  const levelData = useVisualization("levels");
  const data = useVisualization(`duration_${selectedLevel}`);

  useEffect(() => {
    if (data) {
      const top = data.slice(0, 3).map((v) => {
        return { count: v.count, duration: `${v.duration} hour${v.duration == '1' ? '' : 's'}` };
      });
      const rest = data.slice(3);
      const restSum = rest.reduce((acc, v) => acc + parseInt(v.count), 0);

      setNData([...top, { count: restSum, duration: "Other" }]);
    } else {
      setNData(null);
    }
  }, [data]);

  return (
    <div className={classes['flex-center-items']}>
      { levelData ?
        <div className={classes['mb-8']}>
          <label for="level" className={classes.chartLabelCls}>Level</label>
          <select id="level" name="level" value={selectedLevel} onChange={(e) => setSelectedLevel(e.target.value)} className={classes.chartSelectCls}>
            <option value="-">All</option>
            { levelData.filter((level) => level.level).map((level) => (
              <option key={level.level} value={level.level}>{ level.level == "All" ? "Other" : level.level } ({ level.count } courses)</option>
            )) }
          </select>
        </div>
        :<></>
      }
      { nData ?
        <PieChart
          width={600}
          height={600}
        >
          <Pie
            data={nData}
            dataKey={(v) => parseInt(v.count)}
            nameKey="duration"
            innerRadius="25%"
            outerRadius="80%"
            label={v => v.duration}
          >
            {
              nData.map((entry, index) => (
                <Cell
                  key={`slice-${index}`}
                  fill={colors[index % 10]}
                  //fillOpacity={this.state.activeIndex === index ? 1 : 0.25}
                />
              ))
            }
          </Pie>
          <Tooltip />
          <Legend verticalAlign="top" height={36} />
        </PieChart>
      : <></> }
    </div>
  );
}

function PriceVisualization({ classes }) {
  const [nData, setNData] = useState(null);
  const [freeData, setFreeData] = useState(null);
  const [selectedLevel, setSelectedLevel] = useState("-");
  const levelData = useVisualization("levels");
  const data = useVisualization(`price_${selectedLevel}`);

  useEffect(() => {
    if (data) {
      const top = data.slice(0, 15).map((v) => {
        return { count: v.count, price: v.price == 0 ? "Free" : `$${v.price}` };
      });
      const rest = data.slice(15);
      const restSum = rest.reduce((acc, v) => acc + parseInt(v.count), 0);

      setNData([...top, { count: restSum, price: "Other" }].filter(v => v.price != "Free"));

      setFreeData(data.reduce((acc, v) => {
        return [{count: acc[0].count + parseInt(v.count), price: "Free"}];
      }, [ { count: 0, price: "Free" } ]));
    } else {
      setNData(null);
    }
  }, [data]);

  return (
    <div className={classes['flex-center-items']}>
      { levelData ?
        <div className={classes['mb-8']}>
          <label for="level" className={classes.chartLabelCls}>Level</label>
          <select id="level" name="level" value={selectedLevel} onChange={(e) => setSelectedLevel(e.target.value)} className={classes.chartSelectCls}>
            <option value="-">All</option>
            { levelData.filter((level) => level.level).map((level) => (
              <option key={level.level} value={level.level}>{ level.level == "All" ? "Other" : level.level } ({ level.count } courses)</option>
            )) }
          </select>
        </div>
        :<></>
      }
      { nData && freeData ?
        <>
          <PieChart
            width={600}
            height={600}
          >
            <Pie
              data={freeData}
              dataKey={(v) => parseInt(v.count)}
              nameKey="price"
              innerRadius="10%"
              outerRadius="20%"
              label={v => v.price}
            >
              {
                freeData.map((entry, index) => (
                  <Cell
                    key={`slice-${index}`}
                    fill={colorsCategory[index % 10]}
                    //fillOpacity={this.state.activeIndex === index ? 1 : 0.25}
                  />
                ))
              }
            </Pie>

            <Pie
              data={nData}
              dataKey={(v) => parseInt(v.count)}
              nameKey="price"
              innerRadius="40%"
              outerRadius="75%"
              label={v => v.price}
            >
              {
                nData.map((entry, index) => (
                  <Cell
                    key={`slice-${index}`}
                    fill={colors[index % 10]}
                    //fillOpacity={this.state.activeIndex === index ? 1 : 0.25}
                  />
                ))
              }
            </Pie>
            <Tooltip />
            <Legend verticalAlign="top" height={36} />
          </PieChart>
        </>
      : <></> }
    </div>
  );
}

function TermsVisualization({ classes }) {
  const data = useVisualization("terms");

  return (
    <div className={classes['flex-center-items']}>
      { data ?
        <BarChart 
          width={600}
          height={300} 
          data={data} 
          layout="vertical"
          margin={{top: 5, right: 30, left: 20, bottom: 5}}
        >
          <XAxis type="number" allowDecimals={false} />
          <YAxis type="category" dataKey="term" tick={{ fill: '#E5E7EB' }} />
          <Tooltip />
          <Legend verticalAlign="top" height={36} />
          <Bar dataKey="count" fill="#8884d8" name="# terms swiped right">
            {
              data.map((entry, index) => (
                <Cell
                  key={`slice-${index}`}
                  fill={colors[index % 10]}
                  //fillOpacity={this.state.activeIndex === index ? 1 : 0.25}
                />
              ))
            }
          </Bar>
        </BarChart>
        : <></>
      }
    </div>
  );
}