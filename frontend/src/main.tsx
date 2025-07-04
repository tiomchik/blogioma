import ReactDOM from "react-dom/client";
import { createRouter } from "@tanstack/react-router";
import { QueryClient} from "@tanstack/react-query";
import App from "./app";
import "@/app/styles/index.scss";

import { routeTree } from "./routeTree.gen";

const router = createRouter({ routeTree });

declare module "@tanstack/react-router" {
  interface Register {
    router: typeof router;
  }
}

const queryClient = new QueryClient();

const rootElement = document.getElementById("root")!;
if (!rootElement.innerHTML) {
  const root = ReactDOM.createRoot(rootElement);
  root.render(<App queryClient={queryClient} router={router} />);
}
