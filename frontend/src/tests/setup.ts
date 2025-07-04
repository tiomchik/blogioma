import { cleanup } from "@testing-library/react";
import { afterEach, vi } from "vitest";

afterEach(() => {
  vi.clearAllMocks();
  cleanup();
});
