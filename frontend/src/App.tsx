import { Outlet, Link } from "react-router-dom";
import { AppBar, Toolbar, Typography, Container, Box } from "@mui/material";

export default function App(){
  return (
    <Box>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            ParlamentníKontrola.cz
          </Typography>
          <Link to="/" style={{color:"#fff", marginRight:16}}>Dashboard</Link>
          <Link to="/hlasovani" style={{color:"#fff", marginRight:16}}>Hlasování</Link>
          <Link to="/tisky" style={{color:"#fff"}}>Tisky</Link>
        </Toolbar>
      </AppBar>
      <Container sx={{ my: 3 }}>
        <Outlet />
      </Container>
    </Box>
  );
}
