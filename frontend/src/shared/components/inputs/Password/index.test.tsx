import {
  expectErrorMessage,
  expectNoErrorMessage,
  pasteIntoFieldByLabelText,
  renderInputWithFormProvider,
} from "@/tests/utils";
import { beforeEach, describe, test } from "vitest";
import PasswordInput, { PASSWORD_FIELD_LABEL } from "./";
import userEvent from "@testing-library/user-event";
import { ERROR_BLANK, ERROR_TOO_SHORT } from "./errorMessages";

describe("without optional prop", () => {
  beforeEach(() => {
    renderInputWithFormProvider(<PasswordInput />);
  });

  test("displays error of blank password", async () => {
    pasteIntoFieldByLabelText(PASSWORD_FIELD_LABEL, "");
    await userEvent.tab();
    expectErrorMessage(ERROR_BLANK);
  });

  test("displays error of too short password", async () => {
    pasteIntoFieldByLabelText(PASSWORD_FIELD_LABEL, "a");
    await userEvent.tab();
    expectErrorMessage(ERROR_TOO_SHORT);
  });
});

test("doesn't display error of blank field if optional = true", async () => {
  renderInputWithFormProvider(<PasswordInput optional={true} />);
  pasteIntoFieldByLabelText(PASSWORD_FIELD_LABEL, "");
  await userEvent.tab();
  expectNoErrorMessage(ERROR_BLANK);
});
