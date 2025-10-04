export default function PaginatedTable({children, page, onPageChange}:{children:React.ReactNode, page:number, onPageChange:(p:number)=>void}){
  return (
    <div>
      {children}
      <div>
        <button onClick={()=>onPageChange(page-1)} disabled={page<=0}>Předchozí</button>
        <span>Stránka {page+1}</span>
        <button onClick={()=>onPageChange(page+1)}>Další</button>
      </div>
    </div>
  )
}
