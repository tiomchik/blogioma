import { test } from "vitest";
import EmailInput, { EMAIL_FIELD_LABEL } from "./";
import {
  expectErrorMessage,
  pasteIntoFieldByLabelText,
  renderInputWithFormProvider,
} from "@/tests/utils";
import userEvent from "@testing-library/user-event";
import { ERROR_INVALID } from "./errorMessages";

test("should display an error for invalid email", async () => {
  renderInputWithFormProvider(<EmailInput />);
  pasteIntoFieldByLabelText(EMAIL_FIELD_LABEL, "invalid@email");
  await userEvent.tab();
  expectErrorMessage(ERROR_INVALID);
});
