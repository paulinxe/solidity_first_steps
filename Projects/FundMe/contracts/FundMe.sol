// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe
{
    using SafeMathChainlink for uint256;

    mapping(address => uint256) public lusers;
    address private owner;
    AggregatorV3Interface priceFeed;

    constructor(address priceFeedAddress) public
    {
        owner = msg.sender;
        priceFeed = AggregatorV3Interface(priceFeedAddress);
    }

    function deposit() public payable
    {
        uint256 minimumUsdInWei = 1 * 10 ** 18;
        uint256 userUsdInWei = getUsdFromWeiInWei(msg.value);
        require(userUsdInWei >= minimumUsdInWei, "Please, deposit more than one dollar");

        lusers[msg.sender] += msg.value;
    }

    function getEthPriceInWei() public view returns(uint256)
    {
        (
            ,
            int256 answer,
            ,
            ,
            
        ) = priceFeed.latestRoundData();

        return uint256(answer) * 10 ** 10; // Recordemos que el precio viene en gwei
    }

    function getUsdFromWeiInWei(uint256 _wei) public view returns(uint256)
    {
        uint256 weiUsd = _wei * getEthPriceInWei();
        return weiUsd / 10 ** 18;
    }

    modifier onlyOwner
    {
        require(msg.sender == owner, "Nice try");

        _;
    }

    function rugpull() public onlyOwner payable
    {
        msg.sender.transfer(address(this).balance);
    }
}