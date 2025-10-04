export default function HlasovaniTable({data}:{data:any[]}){
  return (
    <table>
      <thead><tr><th>ID</th><th>Datum</th><th>Název</th></tr></thead>
      <tbody>
        {data.map(h=><tr key={h.id_hlasovani}><td>{h.id_hlasovani}</td><td>{h.datum}</td><td>{h.nazev_kratky}</td></tr>)}
      </tbody>
    </table>
  )
}
