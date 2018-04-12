<?php
        $reqFileName = "reqfile.txt";
        $myfile = fopen($reqFileName, "w");
        fwrite($myfile, $_POST["comment"]);
        fclose($myfile);

        $command = escapeshellcmd("./arg2cls_v0.3.py reqfile.txt");
        $output = shell_exec($command);

        $output = str_replace(' ', '&nbsp;',$output);

        echo nl2br($output);

        $command2 = escapeshellcmd('./hist.py');
        shell_exec($command2);
?>
