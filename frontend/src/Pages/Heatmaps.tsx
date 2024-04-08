import { Button, Flex, Image, Select } from "@chakra-ui/react";
import Navbar from "../Components/Navbar";
import { useState } from "react";

const Heatmaps = () => {
  const [week, setWeek] = useState<number>(14);

  const nextWeek = () => {
    if (week < 52) {
      setWeek(week + 1);
    }
  };

  const prevWeek = () => {
    if (week > 0) {
      setWeek(week - 1);
    }
  };

  const handleChangeWeek = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setWeek(Number(event.target.value));
  };

  const heatmapImagePath = require(`../Assets/heatmaps/week_${week + 1}.png`);

  return (
    <Flex direction="column" align="center">
      <Navbar />
      <Flex my="4">
        <Button mr="4" onClick={prevWeek} disabled={week === 0} width="150px">
          Previous Week
        </Button>
        <Select
          onChange={handleChangeWeek}
          value={week}
          width="150px"
          mr="4"
          sx={{ option: { bg: "nugray.400" } }}
        >
          {Array.from({ length: 53 }).map((_, index) => (
            <option key={index} value={index}>
              Week {index + 1}
            </option>
          ))}
        </Select>
        <Button onClick={nextWeek} disabled={week === 53} width="150px">
          Next Week
        </Button>
      </Flex>
      <Flex justify="center" align="center">
        <Image src={heatmapImagePath} alt={`Heatmap for Week ${week}`} />
      </Flex>
    </Flex>
  );
};

export default Heatmaps;
