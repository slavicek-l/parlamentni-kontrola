export default function PoslanecProfileCard({poslanec}:{poslanec:any}){
  return (
    <div style={{border:"1px solid #ccc", padding:16, margin:8}}>
      <h3>{poslanec.jmeno} {poslanec.prijmeni}</h3>
      <p>Strana: {poslanec.strana}</p>
      <p>Kraj: {poslanec.kraj}</p>
    </div>
  )
}
