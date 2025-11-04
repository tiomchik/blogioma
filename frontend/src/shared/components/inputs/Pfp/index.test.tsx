import {
  expectErrorMessage,
  renderInputWithFormProvider,
  uploadDummyPfp,
} from "@/tests/utils";
import { act } from "@testing-library/react";
import { test } from "vitest";
import PfpInput from "./";
import userEvent from "@testing-library/user-event";
import { ERROR_WRONG_FILE_TYPE } from "./errorMessages";

test("displays error of invalid pfp", async () => {
  renderInputWithFormProvider(<PfpInput />);

  uploadDummyPfp("pfp.txt", "text/plain");
  await act(async () => {
    // The first tab is for input, the second for blurring
    await userEvent.tab();
    await userEvent.tab();
  });

  expectErrorMessage(ERROR_WRONG_FILE_TYPE);
});
