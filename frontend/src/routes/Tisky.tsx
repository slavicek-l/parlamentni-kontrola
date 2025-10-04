import { useEffect, useState } from "react";
import axios from "axios";
const API = import.meta.env.VITE_API_BASE || "/api/v1";
export default function Tisky(){
  const [items,setItems]=useState<any[]>([]);
  useEffect(()=>{ axios.get(`${API}/tisky?limit=50`).then(r=>setItems(r.data)); },[]);
  return <ul>{items.map(t=><li key={t.id_tisk}>{t.cislo_tisku} – {t.nazev}</li>)}</ul>;
}
