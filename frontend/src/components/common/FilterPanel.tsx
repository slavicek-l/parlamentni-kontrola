export default function FilterPanel({filters, onChange}:{filters:any, onChange:(f:any)=>void}){
  return (
    <div>
      <input placeholder="Vyhledávání..." onChange={e=>onChange({...filters, q: e.target.value})} />
    </div>
  )
}
