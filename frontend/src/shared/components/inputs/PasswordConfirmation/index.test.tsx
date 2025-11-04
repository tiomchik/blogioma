import {
  expectErrorMessage,
  pasteIntoFieldByLabelText,
  renderInputWithFormProvider,
} from "@/tests/utils";
import { test, beforeEach } from "vitest";
import PasswordConfirmationInput, {
  PASSWORD_CONFIRMATION_FIELD_LABEL,
} from "./";
import { PasswordInput, PASSWORD_FIELD_LABEL } from "@/shared/components";
import userEvent from "@testing-library/user-event";
import { ERROR_BLANK, ERROR_MISMATCH } from "./errorMessages";

beforeEach(() => {
  renderInputWithFormProvider(<PasswordConfirmationInput />);
});

test("displays error of blank password confirmation", async () => {
  pasteIntoFieldByLabelText(PASSWORD_CONFIRMATION_FIELD_LABEL, "");
  await userEvent.tab();
  expectErrorMessage(ERROR_BLANK);
});

test("displays error of mismatched passwords", async () => {
  renderInputWithFormProvider(<PasswordInput />);
  pasteIntoFieldByLabelText(PASSWORD_FIELD_LABEL, "a");
  pasteIntoFieldByLabelText(PASSWORD_CONFIRMATION_FIELD_LABEL, "b");
  await userEvent.tab();
  expectErrorMessage(ERROR_MISMATCH);
});
