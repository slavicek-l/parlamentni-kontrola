import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";
import NavrhySummaryChart from "../components/charts/NavrhySummaryChart";
import NavrhyTrendChart from "../components/charts/NavrhyTrendChart";
const API = import.meta.env.VITE_API_BASE || "/api/v1";

export default function PoslanecProfile(){
  const { id } = useParams();
  const [detail, setDetail] = useState<any>(null);
  const [summary, setSummary] = useState<any[]>([]);
  const [trendy, setTrendy] = useState<any[]>([]);
  const [tisky, setTisky] = useState<any[]>([]);
  useEffect(()=>{
    axios.get(`${API}/poslanci/${id}`).then(r=>setDetail(r.data));
    axios.get(`${API}/statistiky/navrhy/top?limit=1`).then(r=>setSummary(r.data.filter((x:any)=>String(x.id_poslanec)===String(id))));
    axios.get(`${API}/statistiky/navrhy/trendy?bucket=mesic`).then(r=>setTrendy(r.data.filter((x:any)=>String(x.id_poslanec)===String(id))));
    axios.get(`${API}/tisky?limit=50`).then(r=>setTisky(r.data));
  },[id]);
  if(!detail) return <div>Načítání…</div>;
  const celkem = summary.reduce((a:any,b:any)=>a+(b.total||0),0);
  return (
    <div>
      <h2>{detail.jmeno} {detail.prijmeni}</h2>
      <section>
        <h3>Návrhy</h3>
        <p>Celkem návrhů: <b>{celkem}</b></p>
        <NavrhySummaryChart data={summary} />
        <NavrhyTrendChart data={trendy} />
        <h4>Seznam návrhů</h4>
        <ul>
          {tisky.slice(0,20).map(t=><li key={t.id_tisk}>{t.cislo_tisku} – {t.nazev}</li>)}
        </ul>
      </section>
    </div>
  )
}
