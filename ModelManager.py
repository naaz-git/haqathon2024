import os
import qai_hub as hub
from app import ChatApp as App
from qai_hub_models.models.llama_v2_7b_chat_quantized.model import (
    DEFAULT_USER_PROMPT,
    END_TOKENS,
    HF_REPO_NAME,
    HF_REPO_URL,
    MODEL_SPLIT_MAP,
    NUM_KEY_VAL_HEADS,
    NUM_SPLITS,
    Llama2_PromptProcessor_1_Quantized,
    Llama2_PromptProcessor_2_Quantized,
    Llama2_PromptProcessor_3_Quantized,
    Llama2_PromptProcessor_4_Quantized,
    Llama2_TokenGenerator_1_Quantized,
    Llama2_TokenGenerator_2_Quantized,
    Llama2_TokenGenerator_3_Quantized,
    Llama2_TokenGenerator_4_Quantized,
    get_input_prompt_with_tags,
    get_tokenizer,
    prepare_combined_attention_mask,
)
from qai_hub_models.utils.args import (
    get_model_cli_parser,
    get_on_device_demo_parser,
    validate_on_device_demo_args,
)
from qai_hub_models.models.llama_v2_7b_chat_quantized import MODEL_ID, Model
from qai_hub_models.models._shared.llama.model import DEFAULT_INPUT_SEQ_LEN
from qai_hub_models.utils.base_model import BaseModel, TargetRuntime
#from .model import MODEL_ID #might be wrong thing to do


class ModelManager:
    """
    Class for handling operations with Llamav2
    """
    def __init__(self):
        self._context_data = ""
        self._context_data_dir = "./model_data"
        self.is_test = False
        self.available_target_runtimes = [TargetRuntime.QNN]
        self.args = self.get_args()
        self.num_splits=NUM_SPLITS
        self.MAX_OUTPUT_TOKENS = 10
        self.default_device = "Samsung Galaxy S24 (Family)"
        self.default_prompt = "Hi! What is 2+3?"
        self.model_cls = Model
        self.num_key_val_heads = NUM_KEY_VAL_HEADS
        self.model_split_map = MODEL_SPLIT_MAP
        self.hub_model_ids = self.args.hub_model_id.split(",")
        self.hub_device = hub.Device(self.args.device)
        self.hub_device = hub.Device(self.args.device)
        
        self.prompt_processor = self.get_prompt_processor()
        self.token_generator = self.get_token_generator()
        self.app =  App(self.prompt_processor,
                self.token_generator,
                get_input_prompt_with_tags=get_input_prompt_with_tags,
                prepare_combined_attention_mask=prepare_combined_attention_mask,
                tokenizer=get_tokenizer(),
                end_tokens=END_TOKENS,
                num_past_key_val_heads=NUM_KEY_VAL_HEADS,
        )

    def prompt_model(self, user_input):
        """
        Function that takes user_input and combines it with context data to query
        the LLM model. Returns model output

        Input:
        user_input => String

        Output:
        String
        """
        prompt = self._create_prompt(user_input)

        # TODO: UPDATE self._send_prompt_receive_response with LLM functionality
        response = self._send_prompt_receive_response(prompt)
        return response

    def _create_prompt(self, user_input):
        """
        Function that combines context data with user response and returns a prompt

        Input:
        user_input => String

        Output:
        String
        """
        context = self._get_context()
        prompt = f"Answer this: {user_input} based on the following data: {context}"
        return prompt

    def _get_context(self):
        """
        Function that reads context data out of a txt file and returns it as a string

        Output:
        String
        """
        context_files = os.listdir(self._context_data_dir)
        current_context_file = context_files[0]

        with open(f"{self._context_data_dir}/{current_context_file}", "r") as file:
            self._context_data = file.read()
    
    def _send_prompt_receive_response(self, prompt):
        """
        Function that sends prompt to LLM and returns the respnse

        Input:
        prompt => String

        Output:
        String
        """
        self.app.generate_output_prompt(
        prompt,
        max_seq_len=self.args.prompt_processor_input_seq_len,
        max_output_tokens=self.args.max_output_tokens,
        )

        # TODO: Update functionality for real LLM interaction
        return "BeepBoop...I am a Llama"
    def get_prompt_processor (self) : 
        return OnDeviceLlamaModelPipeline(
            self.hub_model_ids[:self.num_splits],
            hub_device=self.hub_device,
            inference_options=self.args.inference_options,
            get_model_class=self._get_model_class,
            num_past_key_val_heads=self.num_key_val_heads,
            model_split_map=self.model_split_map,
        )

    def get_token_generator (self):
        return      OnDeviceLlamaModelPipeline(
            self.hub_model_ids[self.num_splits:],
            hub_device=self.hub_device,
            inference_options=self.args.inference_options,
            get_model_class=self._get_model_class,
            num_past_key_val_heads=self.num_key_val_heads,
            model_split_map=self.model_split_map,
            is_token_generator=True,
        )


    def get_args (self):
        # Demo parameters
        parser = get_model_cli_parser(self.model_cls)
        parser = get_on_device_demo_parser(
            parser,
            add_output_dir=True,
            available_target_runtimes=self.available_target_runtimes,
            default_device=self.default_device,
        )
        parser.add_argument(
            "--prompt",
            type=str,
            default=self.default_prompt,
            help="input prompt.",
        )
        parser.add_argument(
            "--prompt-processor-input-seq-len",
            type=int,
            default=DEFAULT_INPUT_SEQ_LEN,
            help="input sequence length for prompt-processor. This must be less than `max_position_embeddings` set for model.",
        )
        parser.add_argument(
            "--max-output-tokens",
            type=int,
            default=self.MAX_OUTPUT_TOKENS,
            help="max output tokens to generate.",
        )
        args = parser.parse_args([] if self.is_test else None)
        validate_on_device_demo_args(args, MODEL_ID)
        return args
    
    def _get_model_class(split_part: int, is_token_generator: bool = False):
        if split_part < 1 or split_part > 4:
            raise RuntimeError(
                "Incorrect index provided to request Model split class."
                f" Must be within (1-4), provided ({split_part})."
            )

        if is_token_generator:
            return [
                Llama2_TokenGenerator_1_Quantized,
                Llama2_TokenGenerator_2_Quantized,
                Llama2_TokenGenerator_3_Quantized,
                Llama2_TokenGenerator_4_Quantized,
            ][split_part - 1]
        return [
            Llama2_PromptProcessor_1_Quantized,
            Llama2_PromptProcessor_2_Quantized,
            Llama2_PromptProcessor_3_Quantized,
            Llama2_PromptProcessor_4_Quantized,
        ][split_part - 1]




if __name__ == "__main__":
    from Retriever import Retriever

    ret = Retriever()
    ret.retrieve_data("MyTeam")

    mod = ModelManager()
    print(mod.prompt_model("What is the meaning of life?"))
