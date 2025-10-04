import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { Provider } from "react-redux";
import { store } from "./store";
import App from "./App";
import Dashboard from "./routes/Dashboard";
import PoslanecProfile from "./routes/PoslanecProfile";
import Hlasovani from "./routes/Hlasovani";
import HlasovaniDetail from "./routes/HlasovaniDetail";
import Tisky from "./routes/Tisky";
import TiskDetail from "./routes/TiskDetail";
import Compare from "./routes/Compare";

const router = createBrowserRouter([
  { path: "/", element: <App />, children: [
    { index: true, element: <Dashboard /> },
    { path: "poslanec/:id", element: <PoslanecProfile /> },
    { path: "hlasovani", element: <Hlasovani /> },
    { path: "hlasovani/:id", element: <HlasovaniDetail /> },
    { path: "tisky", element: <Tisky /> },
    { path: "tisky/:id", element: <TiskDetail /> },
    { path: "compare", element: <Compare /> },
  ] }
]);

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <Provider store={store}>
      <RouterProvider router={router} />
    </Provider>
  </React.StrictMode>
);
