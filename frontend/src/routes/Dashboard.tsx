import { useEffect, useState } from "react";
import axios from "axios";
import TopNavrhovateleChart from "../components/charts/TopNavrhovateleChart";
const API = import.meta.env.VITE_API_BASE || "/api/v1";

export default function Dashboard(){
  const [data, setData] = useState<any[]>([]);
  useEffect(() => {
    axios.get(`${API}/statistiky/navrhy/top?limit=10`).then(r=>setData(r.data));
  },[]);
  return (
    <>
      <h2>Top navrhovatelé</h2>
      <TopNavrhovateleChart data={data} />
    </>
  );
}
