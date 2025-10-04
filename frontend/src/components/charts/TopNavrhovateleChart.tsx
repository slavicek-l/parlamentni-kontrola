import { Bar } from "react-chartjs-2";
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Tooltip, Legend } from "chart.js";
ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

export default function TopNavrhovateleChart({data}:{data:any[]}){
  const labels = data.map(d=>`#${d.id_poslanec}`);
  return (
    <Bar data={{
      labels,
      datasets: [
        { label: "Navrhovatel", data: data.map(d=>d.navrhovatel||0), backgroundColor: "#1976d2" },
        { label: "Spolu-navrhovatel", data: data.map(d=>d.spolu||0), backgroundColor: "#90caf9" },
      ]
    }} options={{responsive:true, plugins:{legend:{position:"bottom"}}}} />
  )
}
