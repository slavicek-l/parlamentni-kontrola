import { Line } from "react-chartjs-2";
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend } from "chart.js";
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend);

export default function NavrhyTrendChart({data}:{data:any[]}){
  const labels = data.map(d=>d.bucket).sort();
  const counts = data.map(d=>d.total);
  return (
    <Line data={{
      labels,
      datasets:[{label:"Návrhy v čase", data:counts, borderColor:"#1976d2"}]
    }} options={{responsive:true}} />
  )
}
