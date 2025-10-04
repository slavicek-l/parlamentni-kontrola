import { useParams } from "react-router-dom";
export default function TiskDetail(){
  const { id } = useParams();
  return <div>Detail tisku {id}</div>;
}
