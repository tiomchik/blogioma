import { defineConfig, mergeConfig } from "vitest/config";
import viteConfig from "./vite.config.mts";

export default mergeConfig(
  viteConfig,
  defineConfig({
    test: {
      setupFiles: "./src/tests/setup.ts",
      globals: true,
      browser: {
        provider: "playwright",
        enabled: true,
        instances: [{ browser: "chromium" }],
      },
    },
  })
);
