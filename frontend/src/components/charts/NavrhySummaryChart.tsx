import { Doughnut } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
ChartJS.register(ArcElement, Tooltip, Legend);

export default function NavrhySummaryChart({data}:{data:any[]}){
  const total = data.reduce((a,b)=>a+(b.total||0),0);
  const nav = data.reduce((a,b)=>a+(b.navrhovatel||0),0);
  const spol = data.reduce((a,b)=>a+(b.spolu||0),0);
  return (
    <Doughnut data={{
      labels:["Navrhovatel","Spolu-navrhovatel"],
      datasets:[{ data:[nav, spol], backgroundColor:["#1976d2","#90caf9"]}]
    }} />
  )
}
