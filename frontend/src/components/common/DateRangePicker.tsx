export default function DateRangePicker({from, to, onChange}:{from?:string, to?:string, onChange:(from:string, to:string)=>void}){
  return (
    <div>
      <input type="date" value={from||''} onChange={e=>onChange(e.target.value, to||'')} />
      <input type="date" value={to||''} onChange={e=>onChange(from||'', e.target.value)} />
    </div>
  )
}
