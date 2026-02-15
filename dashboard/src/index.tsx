import { createRoot } from "react-dom/client";
import { App } from "./App";
import { MdViewer } from "./MdViewer";

const root = createRoot(document.getElementById("root")!);
const isMdViewer = window.location.pathname.endsWith("md.html");
root.render(isMdViewer ? <MdViewer /> : <App />);
