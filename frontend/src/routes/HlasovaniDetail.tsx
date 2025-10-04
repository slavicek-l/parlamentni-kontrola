import { useParams } from "react-router-dom";
export default function HlasovaniDetail(){
  const { id } = useParams();
  return <div>Detail hlasování {id}</div>;
}
