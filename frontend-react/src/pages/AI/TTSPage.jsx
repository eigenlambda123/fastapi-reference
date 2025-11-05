import { useState } from "react";
import {
  Box,
  Button,
  Textarea,
  VStack,
  Heading,
  useToast,
} from "@chakra-ui/react";
import { textToSpeech } from "../../api/ai";

export default function TTSPage() {
  const [text, setText] = useState("");
  const [audioUrl, setAudioUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const toast = useToast();

  const handleTTS = async () => {
    if (!text.trim()) {
      toast({
        title: "Please enter some text.",
        status: "warning",
        duration: 2000,
      });
      return;
    }

    try {
      setLoading(true);

      const audioBlob = await textToSpeech({ text });
      const url = URL.createObjectURL(audioBlob);
      setAudioUrl(url);
    } catch (error) {
      toast({
        title: "Error generating speech.",
        description: "Please check your input or server connection.",
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
          🗣️ Text-to-Speech
        </Heading>

        <Textarea
          placeholder="Enter text to convert to speech..."
          value={text}
          onChange={(e) => setText(e.target.value)}
          size="md"
          resize="vertical"
        />

        <Button colorScheme="blue" onClick={handleTTS} isLoading={loading}>
          Convert to Speech
        </Button>

        {audioUrl && (
          <Box mt={4}>
            <audio controls src={audioUrl} style={{ width: "100%" }} />
          </Box>
        )}
      </VStack>
    </Box>
  );
}
