import {
  expectErrorMessage,
  pasteIntoFieldByLabelText,
  renderInputWithFormProvider,
} from "@/tests/utils";
import { beforeEach, test } from "vitest";
import PasswordInput, { PASSWORD_FIELD_LABEL } from "./";
import userEvent from "@testing-library/user-event";

beforeEach(() => {
  renderInputWithFormProvider(<PasswordInput />);
});

test("displays error of blank password", async () => {
  pasteIntoFieldByLabelText(PASSWORD_FIELD_LABEL, "");
  await userEvent.tab();
  expectErrorMessage(/Password cannot be blank/);
});

test("displays error of too short password", async () => {
  pasteIntoFieldByLabelText(PASSWORD_FIELD_LABEL, "a");
  await userEvent.tab();
  expectErrorMessage(/Password should be more than \d+ characters long/);
});
