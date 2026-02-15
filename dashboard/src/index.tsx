import { createRoot } from "react-dom/client";
import { useState, useEffect } from "react";
import { App } from "./App";

const root = createRoot(document.getElementById("root")!);
root.render(<App />);
