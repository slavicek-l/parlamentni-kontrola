import { useEffect, useState } from "react";
import axios from "axios";
const API = import.meta.env.VITE_API_BASE || "/api/v1";
export default function Hlasovani(){
  const [items,setItems]=useState<any[]>([]);
  useEffect(()=>{ axios.get(`${API}/hlasovani?limit=50`).then(r=>setItems(r.data)); },[]);
  return <ul>{items.map(h=><li key={h.id_hlasovani}>{h.datum}: {h.nazev_kratky}</li>)}</ul>;
}
