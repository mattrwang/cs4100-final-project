import {
  Button,
  Divider,
  Flex,
  FormLabel,
  HStack,
  Heading,
  Select,
  Text,
  VStack,
  useToast,
} from "@chakra-ui/react";
import Navbar from "../Components/Navbar";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import React, { useState } from "react";
import Loading from "../Components/Loading";

const SnellDensity = () => {
  const [startDate, setStartDate] = useState<Date | null>(new Date());
  const [hour, setHour] = useState<number>(12);
  const [period, setPeriod] = useState<string>("AM");
  const [submitted, setSubmitted] = useState<boolean>(false);
  const [predicted, setPredicted] = useState<boolean>(false);
  const [density, setDensity] = useState<number>(0);

  const toast = useToast();

  const onSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!startDate) {
      toast({
        title: "Error",
        description: "Please select a date",
        status: "error",
        duration: 3000,
        isClosable: true,
      });
      return;
    } else {
      setSubmitted(true);
      try {
        var convert = hour;
        if (period === "PM") {
          convert += 12;
        }
        const response = await fetch("http://localhost:5000/predict", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ date: startDate, time: convert }),
        });
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const responseData = await response.json();
        setDensity(responseData["density"]);
        setPredicted(true);
      } catch (error) {
        console.error("Error:", error);
      }
    }
  };

  return (
    <Flex flexDir="column" align="center">
      <Navbar />
      {!submitted && (
        <form onSubmit={onSubmit}>
          <Flex
            flexDir="column"
            bg="nugray.600"
            p="8"
            mt="50px"
            width="500px"
            align="center"
            justify="center"
          >
            <Heading size="lg">Predict Density:</Heading>
            <HStack mt="20px" spacing={8} align="flex-start">
              <VStack width="200px">
                <FormLabel>Choose the date:</FormLabel>
                <DatePicker
                  selected={startDate}
                  onChange={(date) => setStartDate(date)}
                />
              </VStack>
              <Divider bg="nugray.100" height="160px" orientation="vertical" />
              <VStack width="200px">
                <FormLabel>Choose the time:</FormLabel>
                <Select
                  variant="outline"
                  value={hour}
                  onChange={(e) => setHour(parseInt(e.target.value))}
                  sx={{ option: { bg: "nugray.400" } }}
                >
                  {Array.from({ length: 12 }, (_, i) => (
                    <option key={i + 1} value={i + 1}>
                      {i + 1}
                    </option>
                  ))}
                </Select>
                <Select
                  variant="outline"
                  value={period}
                  onChange={(e) => setPeriod(e.target.value)}
                  sx={{ option: { bg: "nugray.400" } }}
                >
                  <option value="AM">AM</option>
                  <option value="PM">PM</option>
                </Select>
              </VStack>
            </HStack>
            <Button mt="50px" colorScheme="nured" type="submit" color="white">
              Predict
            </Button>
          </Flex>
        </form>
      )}
      {submitted && !predicted && <Loading />}
      {predicted && (
        <Flex
          align="center"
          justify="center"
          bg="nugray.600"
          padding="8"
          width="300px"
          rounded="md"
          shadow="md"
          mt="50px"
          flexDir="column"
        >
          <Heading size="md" textAlign="center">
            Predicted Density:
          </Heading>
          <Text textAlign="center" pt="10px">
            {density.toFixed(0)} new people
          </Text>
        </Flex>
      )}
    </Flex>
  );
};

export default SnellDensity;
