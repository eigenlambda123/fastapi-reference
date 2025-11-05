import { useState } from "react";
import {
  Box,
  Button,
  VStack,
  Heading,
  Text,
  Input,
  useToast,
  Spinner,
} from "@chakra-ui/react";
import { speechToText } from "../../api/ai";

export default function STTPage() {
  const [audioFile, setAudioFile] = useState(null);
  const [transcript, setTranscript] = useState("");
  const [loading, setLoading] = useState(false);
  const toast = useToast();

  const handleFileChange = (e) => {
    setAudioFile(e.target.files[0]);
    setTranscript("");
  };

  const handleTranscribe = async () => {
    if (!audioFile) {
      toast({
        title: "Please upload an audio file.",
        status: "warning",
        duration: 2000,
      });
      return;
    }

    const formData = new FormData();
    formData.append("file", audioFile);

    try {
      setLoading(true);
      const result = await speechToText(formData);
      setTranscript(result.transcription || "No text detected.");
    } catch (err) {
      console.error(err);
      toast({
        title: "Error transcribing audio.",
        description: "Please check the file and try again.",
        status: "error",
        duration: 3000,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box maxW="600px" mx="auto" mt={12}>
      <VStack spacing={4} align="stretch">
        <Heading size="md" textAlign="center">
          🎙️ Speech-to-Text
        </Heading>

        <Input
          type="file"
          accept="audio/*"
          onChange={handleFileChange}
          variant="filled"
        />

        <Button
          colorScheme="blue"
          onClick={handleTranscribe}
          isLoading={loading}
          isDisabled={!audioFile}
        >
          Transcribe Audio
        </Button>

        {loading && (
          <Box textAlign="center">
            <Spinner size="lg" />
          </Box>
        )}

        {transcript && (
          <Box
            borderWidth="1px"
            borderRadius="md"
            p={4}
            mt={4}
            bg="gray.50"
            whiteSpace="pre-wrap"
          >
            <Text>{transcript}</Text>
          </Box>
        )}
      </VStack>
    </Box>
  );
}
