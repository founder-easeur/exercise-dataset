import "@testing-library/jest-dom/vitest";
import { afterEach } from "vitest";
import { cleanup } from "@testing-library/react";

// vitest runs without globals:true, so RTL's auto-cleanup never registers —
// without this, rendered DOM leaks between tests and queries match twice.
afterEach(cleanup);
