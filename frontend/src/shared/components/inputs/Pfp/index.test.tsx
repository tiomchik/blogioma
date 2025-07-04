import {
  expectErrorMessage,
  renderInputWithFormProvider,
  uploadDummyPfp,
} from "@/tests/utils";
import { act } from "@testing-library/react";
import { beforeEach, test } from "vitest";
import PfpInput from "./";
import userEvent from "@testing-library/user-event";

beforeEach(() => {
  renderInputWithFormProvider(<PfpInput />);
});

test("displays error of invalid pfp", async () => {
  uploadDummyPfp("pfp.txt", "text/plain");
  await act(async () => {
    // The first tab is for input, the second for blurring
    await userEvent.tab();
    await userEvent.tab();
  });
  expectErrorMessage(/File is not an image/);
});
