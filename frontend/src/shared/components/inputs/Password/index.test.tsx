import {
  expectErrorMessage,
  expectNoErrorMessage,
  pasteIntoFieldByLabelText,
  renderInputWithFormProvider,
} from "@/tests/utils";
import { beforeEach, describe, test } from "vitest";
import PasswordInput, { PASSWORD_FIELD_LABEL } from "./";
import userEvent from "@testing-library/user-event";

const BLANK_PASSWORD_ERROR_MESSAGE = /Password cannot be blank/;

describe("without optional prop", () => {
  beforeEach(() => {
    renderInputWithFormProvider(<PasswordInput />);
  });

  test("displays error of blank password", async () => {
    pasteIntoFieldByLabelText(PASSWORD_FIELD_LABEL, "");
    await userEvent.tab();
    expectErrorMessage(BLANK_PASSWORD_ERROR_MESSAGE);
  });

  test("displays error of too short password", async () => {
    pasteIntoFieldByLabelText(PASSWORD_FIELD_LABEL, "a");
    await userEvent.tab();
    expectErrorMessage(/Password should be more than \d+ characters long/);
  });
});

test("doesn't display error of blank field if optional = true", async () => {
  renderInputWithFormProvider(<PasswordInput optional={true} />);
  pasteIntoFieldByLabelText(PASSWORD_FIELD_LABEL, "");
  await userEvent.tab();
  expectNoErrorMessage(BLANK_PASSWORD_ERROR_MESSAGE);
});
