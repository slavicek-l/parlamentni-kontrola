export default function TiskyTable({data}:{data:any[]}){
  return (
    <table>
      <thead><tr><th>ID</th><th>Číslo</th><th>Název</th></tr></thead>
      <tbody>
        {data.map(t=><tr key={t.id_tisk}><td>{t.id_tisk}</td><td>{t.cislo_tisku}</td><td>{t.nazev}</td></tr>)}
      </tbody>
    </table>
  )
}
